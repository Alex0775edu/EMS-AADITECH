from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Notice, TARGET_CHOICES

@login_required
def notice_list(request):
    notices = Notice.objects.all()
    if not request.user.is_superuser:
        notices = notices.filter(
            Q(created_by=request.user) | Q(created_by__institution_id=request.user.institution_id)
        ).distinct()
    target = request.GET.get('target', '').strip()
    if target:
        notices = notices.filter(target=target)
    query = request.GET.get('q', '').strip()
    if query:
        notices = notices.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(
        request,
        'notices/notice_list.html',
        {'notices': notices.order_by('-publish_date'), 'target_choices': TARGET_CHOICES},
    )

@login_required
def notice_add(request):
    if request.user.role == 'STUDENT':
        messages.error(request, 'Students are not allowed to create notices.')
        return redirect('notices:notice_list')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        target = request.POST.get('target', 'all')
        expiry_date = request.POST.get('valid_until') or None

        Notice.objects.create(
            title=title,
            description=content,
            target=target,
            expiry_date=expiry_date,
            institution=None,
            created_by=request.user,
        )
        return redirect('notices:notice_list')
    return render(request, 'notices/notice_add.html')
