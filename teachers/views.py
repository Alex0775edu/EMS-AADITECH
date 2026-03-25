from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from accounts.models import User
from core.models import Institution as CoreInstitution
from .models import Teacher

def _placeholder(request, title, message, back_url=None):
    return render(
        request,
        'base/placeholder.html',
        {
            'title': title,
            'message': message,
            'back_url': back_url,
        },
    )

@login_required
def teacher_list(request):
    if request.user.role == 'STUDENT':
        messages.error(request, 'Students are not allowed to view teacher management.')
        return redirect('dashboard:dashboard')

    teachers = Teacher.objects.select_related('user')
    if not request.user.is_superuser:
        teachers = teachers.filter(institution_id=request.user.institution_id)
    query = request.GET.get('q', '').strip()
    if query:
        teachers = teachers.filter(
            Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
            | Q(user__email__icontains=query)
            | Q(subject__icontains=query)
            | Q(qualification__icontains=query)
        )
    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})

@login_required
def teacher_add(request):
    if request.user.role == 'STUDENT':
        messages.error(request, 'Students are not allowed to create teacher records.')
        return redirect('teachers:teacher_list')

    if request.method == 'POST':
        institution = request.user.institution
        if request.user.is_superuser:
            institution_id = request.POST.get('institution_id')
            institution = CoreInstitution.objects.filter(pk=institution_id).first()

        if not institution:
            messages.error(request, 'Please select a valid institution.')
            return redirect('teachers:teacher_add')

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        qualification = request.POST.get('qualification', '').strip()
        subject = request.POST.get('subject', '').strip() or 'General'
        institute_id = request.POST.get('institute_id', '').strip()
        dob = request.POST.get('date_of_birth', '').strip()

        if not first_name or not email or not qualification:
            messages.error(request, 'First name, email and qualification are required.')
            return redirect('teachers:teacher_add')

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'A user with this email already exists.')
            return redirect('teachers:teacher_add')

        if institute_id and User.objects.filter(institute_id__iexact=institute_id).exists():
            messages.error(request, 'Institute ID is already in use.')
            return redirect('teachers:teacher_add')

        username_base = email.split('@')[0].replace(' ', '').lower()
        username = username_base
        i = 1
        while User.objects.filter(username=username).exists():
            i += 1
            username = f'{username_base}{i}'

        if not institute_id:
            institute_id = f"T{timezone.now().strftime('%Y%m%d%H%M%S')}"

        default_password = 'Teacher@123'
        if dob:
            try:
                default_password = datetime.strptime(dob, '%Y-%m-%d').strftime('%d%m%Y')
            except ValueError:
                pass

        with transaction.atomic():
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                role='TEACHER',
                institute_id=institute_id,
                institution=institution,
                date_of_birth=dob or None,
            )
            user.set_password(default_password)
            user.save()

            Teacher.objects.create(
                user=user,
                institution=institution,
                subject=subject[:100],
                qualification=qualification[:100],
            )

        messages.success(request, f'Teacher created. Default password: {default_password}')
        return redirect('teachers:teacher_list')
    institutions = CoreInstitution.objects.all().order_by('name') if request.user.is_superuser else []
    return render(request, 'teachers/teacher_add.html', {'institutions': institutions})


@login_required
def teacher_detail(request, teacher_id):
    return _placeholder(
        request,
        'Teacher Profile',
        'Detailed teacher profiles will be available soon.',
        back_url='/teachers/',
    )


@login_required
def teacher_edit(request, teacher_id):
    return _placeholder(
        request,
        'Edit Teacher',
        'Teacher profile editing will be enabled in the next release.',
        back_url='/teachers/',
    )


@login_required
def teacher_schedule(request, teacher_id):
    return _placeholder(
        request,
        'Teacher Schedule',
        'Scheduling and timetable management are coming soon.',
        back_url='/teachers/',
    )
