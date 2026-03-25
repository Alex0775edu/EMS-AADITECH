from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from accounts.models import User
from core.models import Institution as CoreInstitution
from .models import Student

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
def student_list(request):
    students = Student.objects.select_related('user')
    if request.user.role == 'STUDENT':
        students = students.filter(user=request.user)
    elif not request.user.is_superuser:
        students = students.filter(institution_id=request.user.institution_id)
    query = request.GET.get('q', '').strip()
    if query:
        students = students.filter(
            Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
            | Q(user__email__icontains=query)
            | Q(roll_no__icontains=query)
            | Q(class_name__icontains=query)
            | Q(section__icontains=query)
        )
    return render(request, 'students/student_list.html', {'students': students})

@login_required
def student_add(request):
    if request.user.role == 'STUDENT':
        messages.error(request, 'Students are not allowed to create records.')
        return redirect('students:student_list')

    if request.method == 'POST':
        institution = request.user.institution
        if request.user.is_superuser:
            institution_id = request.POST.get('institution_id')
            institution = CoreInstitution.objects.filter(pk=institution_id).first()

        if not institution:
            messages.error(request, 'Please select a valid institution.')
            return redirect('students:student_add')

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        institute_id = request.POST.get('institute_id', '').strip()
        roll_no = request.POST.get('roll_no', '').strip()
        class_name = request.POST.get('class_name', '').strip()
        section = request.POST.get('section', '').strip()
        dob = request.POST.get('date_of_birth', '').strip()

        if not all([first_name, email, roll_no, class_name, section]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('students:student_add')

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'A user with this email already exists.')
            return redirect('students:student_add')

        if institute_id and User.objects.filter(institute_id__iexact=institute_id).exists():
            messages.error(request, 'Institute ID is already in use.')
            return redirect('students:student_add')

        username_base = email.split('@')[0].replace(' ', '').lower()
        username = username_base
        i = 1
        while User.objects.filter(username=username).exists():
            i += 1
            username = f'{username_base}{i}'

        if not institute_id:
            institute_id = f"S{timezone.now().strftime('%Y%m%d%H%M%S')}"

        default_password = 'Student@123'
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
                role='STUDENT',
                institute_id=institute_id,
                institution=institution,
                date_of_birth=dob or None,
            )
            user.set_password(default_password)
            user.save()
            Student.objects.create(
                user=user,
                institution=institution,
                roll_no=roll_no,
                class_name=class_name,
                section=section,
            )

        messages.success(request, f'Student created. Default password: {default_password}')
        return redirect('students:student_list')

    institutions = CoreInstitution.objects.all().order_by('name') if request.user.is_superuser else []
    return render(request, 'students/student_add.html', {'institutions': institutions})

@login_required
def student_detail(request, student_id):
    qs = Student.objects.select_related('user')
    if request.user.role == 'STUDENT':
        qs = qs.filter(user=request.user)
    elif not request.user.is_superuser:
        qs = qs.filter(institution_id=request.user.institution_id)
    student = qs.filter(id=student_id).first()
    if not student:
        raise Http404('Student not found')
    return render(request, 'students/student_detail.html', {'student': student})


@login_required
def student_edit(request, student_id):
    return _placeholder(
        request,
        'Edit Student',
        'Student profile editing will be available in the next upgrade.',
        back_url='/students/',
    )


@login_required
def student_attendance(request, student_id):
    return _placeholder(
        request,
        'Student Attendance',
        'Attendance drill-down is coming soon with detailed analytics.',
        back_url='/attendance/report/',
    )
