from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Thread, SupportTicket


@login_required
def thread_list(request):
    threads = Thread.objects.order_by('-created_at')[:20]
    return render(request, 'communications/threads.html', {'threads': threads})


@login_required
def ticket_list(request):
    tickets = SupportTicket.objects.order_by('-created_at')[:20]
    return render(request, 'communications/tickets.html', {'tickets': tickets})
