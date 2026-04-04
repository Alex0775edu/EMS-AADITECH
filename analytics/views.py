from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import EventLog, DailyMetric


@login_required
def event_list(request):
    if not _can_view_analytics(request.user):
        messages.error(request, 'You do not have access to analytics.')
        return redirect('dashboard:dashboard')

    event_type = (request.GET.get('type') or '').strip().lower()
    qs = EventLog.objects.select_related('user').order_by('-created_at')
    if event_type:
        qs = qs.filter(event_type=event_type)
    events = qs[:200]
    return render(request, 'analytics/events.html', {'events': events, 'event_type': event_type})


@login_required
def summary(request):
    if not _can_view_analytics(request.user):
        messages.error(request, 'You do not have access to analytics.')
        return redirect('dashboard:dashboard')

    try:
        days = int(request.GET.get('days', 30))
    except ValueError:
        days = 30
    days = max(7, min(days, 365))
    since_date = (timezone.now() - timedelta(days=days - 1)).date()

    events = EventLog.objects.filter(created_at__date__gte=since_date)
    page_views_qs = events.filter(event_type='page_view')
    logins_qs = events.filter(event_type='login')

    total_page_views = page_views_qs.count()
    total_logins = logins_qs.count()
    unique_visitors = page_views_qs.exclude(ip_address__isnull=True).values('ip_address').distinct().count()
    unique_logins = logins_qs.exclude(user__isnull=True).values('user_id').distinct().count()

    recent_logins = logins_qs.select_related('user').order_by('-created_at')[:12]
    recent_views = page_views_qs.select_related('user').order_by('-created_at')[:12]

    metrics = DailyMetric.objects.filter(
        metric__in=['page_view', 'login'],
        metric_date__gte=since_date,
    ).order_by('metric_date')

    series = []
    if metrics.exists():
        metric_map = {(m.metric_date, m.metric): int(m.value) for m in metrics}
        for idx in range(days):
            day = since_date + timedelta(days=idx)
            series.append({
                'date': day,
                'page_views': metric_map.get((day, 'page_view'), 0),
                'logins': metric_map.get((day, 'login'), 0),
            })
    else:
        grouped = events.annotate(day=TruncDate('created_at')).values('day', 'event_type').annotate(count=Count('id'))
        metric_map = {(row['day'], row['event_type']): row['count'] for row in grouped}
        for idx in range(days):
            day = since_date + timedelta(days=idx)
            series.append({
                'date': day,
                'page_views': metric_map.get((day, 'page_view'), 0),
                'logins': metric_map.get((day, 'login'), 0),
            })

    context = {
        'days': days,
        'since_date': since_date,
        'total_page_views': total_page_views,
        'total_logins': total_logins,
        'unique_visitors': unique_visitors,
        'unique_logins': unique_logins,
        'recent_logins': recent_logins,
        'recent_views': recent_views,
        'series': series,
    }
    return render(request, 'analytics/summary.html', context)


def _can_view_analytics(user):
    return bool(getattr(user, 'is_superuser', False))
