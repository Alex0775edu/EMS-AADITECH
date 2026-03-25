from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import EventLog


@login_required
def event_list(request):
    events = EventLog.objects.order_by('-created_at')[:40]
    return render(request, 'analytics/events.html', {'events': events})
