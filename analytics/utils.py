import logging
from decimal import Decimal

from django.utils import timezone
from django.db.models import F

from .models import EventLog, DailyMetric

logger = logging.getLogger(__name__)


def get_client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def _safe_str(value, limit=200):
    if value is None:
        return ''
    text = str(value)
    if len(text) <= limit:
        return text
    return text[:limit]


def log_event(request, event_type, metadata=None, user=None):
    metadata = metadata or {}
    try:
        ip_address = get_client_ip(request)
        if ip_address:
            metadata.setdefault('ip', ip_address)

        user_obj = user if user is not None else getattr(request, 'user', None)
        if user_obj is not None and not getattr(user_obj, 'is_authenticated', False):
            user_obj = None

        EventLog.objects.create(
            user=user_obj,
            event_type=event_type,
            metadata=metadata,
            ip_address=ip_address,
        )
        _increment_daily_metric(request, event_type)
    except Exception:
        logger.exception('Failed to log analytics event %s', event_type)


def _increment_daily_metric(request, event_type):
    metric_date = timezone.now().date()
    institution = None
    user = getattr(request, 'user', None)
    if user and getattr(user, 'is_authenticated', False):
        institution = getattr(user, 'institution', None)

    qs = DailyMetric.objects.filter(
        institution=institution,
        metric=event_type,
        metric_date=metric_date,
    )
    if qs.exists():
        qs.update(value=F('value') + Decimal('1'))
    else:
        DailyMetric.objects.create(
            institution=institution,
            metric=event_type,
            value=Decimal('1'),
            metric_date=metric_date,
        )
