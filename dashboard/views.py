import json
from datetime import date, timedelta, datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.models import User
from attendance.models import Attendance
from core.models import Institution as CoreInstitution
from exams.models import Exam
from notices.models import Notice
from students.models import Student
from teachers.models import Teacher

from .models import (
    ActivityLog,
    Announcement,
    Assignment,
    AssignmentSubmission,
    Course,
    CourseEnrollment,
    FeePayment,
    StudentPerformance,
)

DEFAULT_PREFERENCES = {
    'notify_email': True,
    'notify_sms': False,
    'notify_push': True,
    'language': 'en',
    'timezone': getattr(settings, 'TIME_ZONE', 'UTC'),
    'date_format': 'DD MMM YYYY',
    'reduced_motion': False,
    'high_contrast': False,
    'large_text': False,
}


def home(request):
    context = {
        'total_students': Student.objects.count(),
        'total_teachers': Teacher.objects.count(),
        'institutes_supported': Student.objects.values('institution').distinct().count(),
    }
    return render(request, 'home/index.html', context)


@login_required
def dashboard(request):
    if request.user.is_superuser or request.user.role == 'ADMIN':
        return admin_dashboard(request)
    if request.user.role == 'TEACHER':
        return teacher_dashboard(request)
    if request.user.role == 'STUDENT':
        return student_dashboard(request)
    return admin_dashboard(request)


@login_required
def admin_dashboard(request):
    total_students = _scoped_queryset(request, Student.objects).count()
    total_teachers = _scoped_queryset(request, Teacher.objects).count()
    pending_fees_count = _scoped_queryset(request, FeePayment.objects, 'student__institution').filter(status='PENDING').count()
    active_classes_count = _scoped_queryset(request, Course.objects, 'institute').count()
    recent_notices = _scoped_notices(request).order_by('-id')[:5]

    chart_labels, attendance_data, performance_data = _dashboard_trends(request)

    return render(
        request,
        'dashboard/dashboard.html',
        {
            'total_students': total_students,
            'total_teachers': total_teachers,
            'pending_fees_count': pending_fees_count,
            'active_classes_count': active_classes_count,
            'recent_notices': recent_notices,
            'chart_labels': json.dumps(chart_labels),
            'attendance_data': json.dumps(attendance_data),
            'performance_data': json.dumps(performance_data),
        },
    )


def _dashboard_trends(request):
    today = timezone.now().date().replace(day=1)
    months = [today - timedelta(days=30 * i) for i in range(5, -1, -1)]
    labels = [m.strftime('%b %Y') for m in months]

    attendance = []
    performance = []

    for m in months:
        month = m.month
        year = m.year

        attendance_qs = _scoped_queryset(request, Attendance.objects, 'student__institution')
        total = attendance_qs.filter(date__year=year, date__month=month).count()
        present = attendance_qs.filter(date__year=year, date__month=month, status='PRESENT').count()
        attendance_pct = round((present / total) * 100, 2) if total else 0
        attendance.append(attendance_pct)

        perf_qs = _scoped_queryset(request, StudentPerformance.objects, 'student__institution')
        avg_score = (
            perf_qs.filter(graded_at__year=year, graded_at__month=month)
            .aggregate(avg=Avg('score'))
            .get('avg')
        )
        performance.append(round(avg_score, 2) if avg_score is not None else 0)

    return labels, attendance, performance


@login_required
def teacher_dashboard(request):
    return render(request, 'dashboard/teacher_dashboard.html')


@login_required
def student_dashboard(request):
    assignments = _scoped_queryset(request, Assignment.objects, 'institute').order_by('-created_at')[:5]
    exams = _scoped_exams(request).order_by('date')[:5]
    return render(request, 'dashboard/student_dashboard.html', {'assignments': assignments, 'exams': exams})


@login_required
def students_page(request):
    students = _scoped_queryset(request, Student.objects.select_related('user'))
    if request.user.role == 'STUDENT':
        students = students.filter(user=request.user)
    return render(request, 'dashboard/pages/students.html', {'students': students})


@login_required
def teachers_page(request):
    if request.user.role == 'STUDENT':
        messages.error(request, 'Students can only view their own dashboard data.')
        return redirect('dashboard:dashboard')

    teachers = _scoped_queryset(request, Teacher.objects.select_related('user'))
    return render(request, 'dashboard/pages/teachers.html', {'teachers': teachers})


@login_required
def courses_page(request):
    courses = _scoped_queryset(request, Course.objects.select_related('teacher'), 'institute')
    courses_list = list(courses)
    enrollments = None
    progress_map = {}
    if request.user.role == 'STUDENT':
        enrollments = CourseEnrollment.objects.select_related('course').filter(student__user=request.user)
        progress_map = {enrollment.course_id: enrollment.progress_percent for enrollment in enrollments}
        for course in courses_list:
            course.progress_percent = progress_map.get(course.id)
    return render(
        request,
        'dashboard/pages/courses.html',
        {
            'courses': courses_list,
            'enrollments': enrollments,
            'progress_map': progress_map,
        },
    )


@login_required
def attendance_page(request):
    records = _scoped_queryset(
        request,
        Attendance.objects.select_related('student', 'student__user').order_by('-date'),
        'student__institution',
    )
    if request.user.role == 'STUDENT':
        records = records.filter(student__user=request.user)
    records = records[:100]
    return render(request, 'dashboard/pages/attendance.html', {'records': records})


@login_required
def assignments_page(request):
    data = _scoped_queryset(request, Assignment.objects.select_related('course').order_by('-created_at'), 'institute')
    assignments = list(data)
    submissions = {}
    if request.user.role == 'STUDENT':
        submissions = {
            s.assignment_id: s
            for s in AssignmentSubmission.objects.filter(student__user=request.user).select_related('assignment')
        }
        for assignment in assignments:
            assignment.submission = submissions.get(assignment.id)
    return render(
        request,
        'dashboard/pages/assignments.html',
        {
            'assignments': assignments,
            'submissions': submissions,
        },
    )


@login_required
def assignment_submit(request, assignment_id):
    assignment = _scoped_queryset(
        request,
        Assignment.objects.select_related('course'),
        'institute',
    ).filter(pk=assignment_id).first()

    if not assignment:
        messages.error(request, 'Assignment not found.')
        return redirect('dashboard:assignments_page')

    if request.user.role != 'STUDENT':
        messages.error(request, 'Only students can submit assignments.')
        return redirect('dashboard:assignments_page')

    student = getattr(request.user, 'student_profile', None)
    if not student:
        messages.error(request, 'Student profile is required to submit assignments.')
        return redirect('dashboard:assignments_page')

    submission = AssignmentSubmission.objects.filter(assignment=assignment, student=student).first()

    if request.method == 'POST':
        attachment = request.FILES.get('attachment')
        notes = request.POST.get('notes', '').strip()

        if not attachment and not notes:
            messages.error(request, 'Please upload a file or add submission notes.')
            return redirect('dashboard:assignment_submit', assignment_id=assignment_id)

        if attachment:
            allowed_types = {
                'application/pdf',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/msword',
                'image/png',
                'image/jpeg',
            }
            max_size = 10 * 1024 * 1024
            if attachment.content_type not in allowed_types:
                messages.error(request, 'Only PDF, DOCX, or image uploads are allowed.')
                return redirect('dashboard:assignment_submit', assignment_id=assignment_id)
            if attachment.size > max_size:
                messages.error(request, 'File size must be under 10 MB.')
                return redirect('dashboard:assignment_submit', assignment_id=assignment_id)

        if submission:
            submission.attachment = attachment or submission.attachment
            submission.notes = notes or submission.notes
            submission.status = 'RESUBMITTED'
            submission.save(update_fields=['attachment', 'notes', 'status'])
            messages.success(request, 'Assignment re-submitted successfully.')
        else:
            AssignmentSubmission.objects.create(
                assignment=assignment,
                student=student,
                attachment=attachment,
                notes=notes,
                status='SUBMITTED',
            )
            messages.success(request, 'Assignment submitted successfully.')

        return redirect('dashboard:assignments_page')

    return render(
        request,
        'dashboard/pages/assignment_submit.html',
        {
            'assignment': assignment,
            'submission': submission,
        },
    )


@login_required
def search(request):
    query = request.GET.get('q', '').strip()
    students = teachers = courses = notices = []

    if query:
        students_qs = _scoped_queryset(
            request,
            Student.objects.select_related('user'),
        ).filter(
            Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
            | Q(user__username__icontains=query)
            | Q(roll_no__icontains=query)
        )
        if request.user.role == 'STUDENT':
            students_qs = students_qs.filter(user=request.user)

        teachers_qs = _scoped_queryset(
            request,
            Teacher.objects.select_related('user'),
        ).filter(
            Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
            | Q(user__username__icontains=query)
            | Q(subject__icontains=query)
        )

        courses_qs = _scoped_queryset(
            request,
            Course.objects.select_related('teacher'),
            'institute',
        ).filter(
            Q(name__icontains=query)
            | Q(code__icontains=query)
            | Q(description__icontains=query)
        )

        notices_qs = _scoped_notices(request).filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

        students = students_qs[:12]
        teachers = teachers_qs[:12]
        courses = courses_qs[:12]
        notices = notices_qs[:8]

    return render(
        request,
        'dashboard/pages/search.html',
        {
            'query': query,
            'students': students,
            'teachers': teachers,
            'courses': courses,
            'notices': notices,
        },
    )


@login_required
def exams_page(request):
    return render(request, 'dashboard/pages/exams.html', {'exams': _scoped_exams(request).order_by('date')})


@login_required
def fees_page(request):
    fees = _scoped_queryset(request, FeePayment.objects.order_by('-created_at'), 'student__institution')
    if request.user.role == 'STUDENT':
        fees = fees.filter(student__user=request.user)
    return render(request, 'dashboard/pages/fees.html', {'fees': fees})


@login_required
def notices_page(request):
    return render(request, 'dashboard/pages/notices.html', {'notices': _scoped_notices(request).order_by('-id')})


@login_required
def notifications_page(request):
    notices = _scoped_notices(request).order_by('-id')[:12]
    logs = ActivityLog.objects.select_related('user').order_by('-created_at')
    if not request.user.is_superuser and request.user.institution_id:
        logs = logs.filter(user__institution_id=request.user.institution_id)
    return render(request, 'dashboard/pages/notifications.html', {'notices': notices, 'logs': logs[:15]})


@login_required
def messaging_page(request):
    students = _scoped_queryset(request, Student.objects.select_related('user'))[:6]
    teachers = _scoped_queryset(request, Teacher.objects.select_related('user'))[:6]
    if request.user.role == 'STUDENT':
        students = Student.objects.none()
    if request.user.role == 'TEACHER':
        teachers = Teacher.objects.none()
    return render(
        request,
        'dashboard/pages/messaging.html',
        {
            'students': students,
            'teachers': teachers,
        },
    )


@login_required
def results_page(request):
    performance = _scoped_queryset(
        request,
        StudentPerformance.objects.select_related('student', 'course').order_by('-graded_at'),
        'student__institution',
    )
    if request.user.role == 'STUDENT':
        performance = performance.filter(student__user=request.user)
    performance = performance[:50]
    return render(request, 'dashboard/pages/results.html', {'performance': performance})


@login_required
def payments_page(request):
    fees = _scoped_queryset(request, FeePayment.objects.order_by('-created_at'), 'student__institution')
    if request.user.role == 'STUDENT':
        fees = fees.filter(student__user=request.user)

    totals = fees.aggregate(
        pending_total=Sum('amount', filter=Q(status='PENDING')),
        paid_total=Sum('amount', filter=Q(status='PAID')),
    )

    pending_total = totals.get('pending_total') or 0
    paid_total = totals.get('paid_total') or 0
    total_amount = pending_total + paid_total
    paid_ratio = round((paid_total / total_amount) * 100, 2) if total_amount else 0

    return render(
        request,
        'dashboard/pages/payments.html',
        {
            'fees': fees[:50],
            'pending_total': pending_total,
            'paid_total': paid_total,
            'total_amount': total_amount,
            'paid_ratio': paid_ratio,
        },
    )


@login_required
def settings_page(request):
    prefs = _user_preferences(request.user)
    return render(request, 'dashboard/pages/settings.html', {'prefs': prefs})


@require_POST
@login_required
def settings_update_profile(request):
    user = request.user
    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()
    email = request.POST.get('email', '').strip().lower()
    institute_id = request.POST.get('institute_id', '').strip()
    dob = request.POST.get('date_of_birth', '').strip()

    if email and User.objects.exclude(pk=user.pk).filter(email__iexact=email).exists():
        messages.error(request, 'Email address is already in use.')
        return redirect('dashboard:settings_page')

    if institute_id and User.objects.exclude(pk=user.pk).filter(institute_id__iexact=institute_id).exists():
        messages.error(request, 'Institute ID is already in use.')
        return redirect('dashboard:settings_page')

    if dob:
        try:
            user.date_of_birth = datetime.strptime(dob, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Date of birth must be in YYYY-MM-DD format.')
            return redirect('dashboard:settings_page')
    else:
        user.date_of_birth = None

    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.institute_id = institute_id or None
    user.save(
        update_fields=['first_name', 'last_name', 'email', 'institute_id', 'date_of_birth']
    )
    messages.success(request, 'Profile updated successfully.')
    return redirect('dashboard:settings_page')


@require_POST
@login_required
def settings_change_password(request):
    user = request.user
    current_password = request.POST.get('current_password', '')
    new_password = request.POST.get('new_password', '')
    confirm_password = request.POST.get('confirm_password', '')

    if not user.check_password(current_password):
        messages.error(request, 'Current password is incorrect.')
        return redirect('dashboard:settings_page')

    if not new_password or len(new_password) < 8:
        messages.error(request, 'New password must be at least 8 characters.')
        return redirect('dashboard:settings_page')

    if new_password != confirm_password:
        messages.error(request, 'New password confirmation does not match.')
        return redirect('dashboard:settings_page')

    user.set_password(new_password)
    user.save(update_fields=['password'])
    update_session_auth_hash(request, user)
    messages.success(request, 'Password updated successfully.')
    return redirect('dashboard:settings_page')


@require_POST
@login_required
def settings_mfa(request):
    enabled = bool(request.POST.get('mfa_enabled'))
    request.user.mfa_enabled = enabled
    request.user.save(update_fields=['mfa_enabled'])
    status = 'enabled' if enabled else 'disabled'
    messages.success(request, f'MFA {status} for your account.')
    return redirect('dashboard:settings_page')


@require_POST
@login_required
def settings_data_download(request):
    user = request.user
    payload = {
        'generated_at': timezone.now().isoformat(),
        'user': {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'role': user.role,
            'institute_id': user.institute_id,
            'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None,
            'institution_id': user.institution_id,
            'is_active': user.is_active,
            'mfa_enabled': user.mfa_enabled,
            'consent_opt_in': user.consent_opt_in,
        },
        'preferences': _user_preferences(user),
        'student_profile': None,
        'teacher_profile': None,
    }

    student = getattr(user, 'student_profile', None)
    if student:
        payload['student_profile'] = {
            'roll_no': student.roll_no,
            'class_name': student.class_name,
            'section': student.section,
            'institution_id': student.institution_id,
        }

    teacher = getattr(user, 'teacher_profile', None)
    if teacher:
        payload['teacher_profile'] = {
            'subject': teacher.subject,
            'qualification': teacher.qualification,
            'institution_id': teacher.institution_id,
        }

    response = HttpResponse(
        json.dumps(payload, indent=2, default=str),
        content_type='application/json',
    )
    response['Content-Disposition'] = 'attachment; filename="ems-account-data.json"'
    return response


@require_POST
@login_required
def settings_delete_account(request):
    confirm_text = request.POST.get('confirm_text', '').strip().upper()
    if confirm_text != 'DELETE':
        messages.error(request, 'Type DELETE to confirm account removal.')
        return redirect('dashboard:settings_page')

    request.user.is_active = False
    request.user.save(update_fields=['is_active'])
    logout(request)
    return redirect('home')


@require_POST
@login_required
def settings_consent(request):
    consent = request.POST.get('consent')
    if consent not in {'opt_in', 'opt_out'}:
        messages.error(request, 'Please choose a valid consent option.')
        return redirect('dashboard:settings_page')

    request.user.consent_opt_in = consent == 'opt_in'
    request.user.save(update_fields=['consent_opt_in'])
    messages.success(request, 'Consent preferences updated.')
    return redirect('dashboard:settings_page')


@require_POST
@login_required
def settings_notifications(request):
    updates = {
        'notify_email': bool(request.POST.get('notify_email')),
        'notify_sms': bool(request.POST.get('notify_sms')),
        'notify_push': bool(request.POST.get('notify_push')),
    }
    _update_user_preferences(request.user, updates)
    messages.success(request, 'Notification preferences updated.')
    return redirect('dashboard:settings_page')


@require_POST
@login_required
def settings_language(request):
    language = request.POST.get('language', 'en').strip() or 'en'
    tz = request.POST.get('timezone', getattr(settings, 'TIME_ZONE', 'UTC')).strip()
    date_format = request.POST.get('date_format', 'DD MMM YYYY').strip() or 'DD MMM YYYY'
    _update_user_preferences(
        request.user,
        {
            'language': language,
            'timezone': tz,
            'date_format': date_format,
        },
    )
    messages.success(request, 'Language and region settings updated.')
    return redirect('dashboard:settings_page')


@require_POST
@login_required
def settings_accessibility(request):
    updates = {
        'reduced_motion': bool(request.POST.get('reduced_motion')),
        'high_contrast': bool(request.POST.get('high_contrast')),
        'large_text': bool(request.POST.get('large_text')),
    }
    _update_user_preferences(request.user, updates)
    messages.success(request, 'Accessibility settings updated.')
    return redirect('dashboard:settings_page')


@login_required
def reports_page(request):
    performance = _scoped_queryset(
        request,
        StudentPerformance.objects.select_related('student', 'course').order_by('-graded_at'),
        'student__institution',
    )

    if request.user.role == 'STUDENT':
        performance = performance.filter(student__user=request.user)

    performance = performance[:30]

    logs = ActivityLog.objects.none()
    if request.user.role != 'STUDENT':
        logs = ActivityLog.objects.select_related('user')
        if not request.user.is_superuser and request.user.institution_id:
            logs = logs.filter(user__institution_id=request.user.institution_id)

    return render(
        request,
        'dashboard/pages/reports.html',
        {
            'performance': performance,
            'logs': logs[:50],
        },
    )


@login_required
def data_hub(request):
    if not (request.user.is_superuser or request.user.role == 'ADMIN'):
        messages.error(request, 'Only admin or superuser can add data from this page.')
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        action = request.POST.get('action', '').strip()
        institution_id = request.POST.get('institution_id') or request.GET.get('institution_id')
        try:
            if action == 'add_student':
                _add_student(request)
                messages.success(request, 'Student created successfully.')
            elif action == 'add_teacher':
                _add_teacher(request)
                messages.success(request, 'Teacher created successfully.')
            elif action == 'add_course':
                _add_course(request)
                messages.success(request, 'Course created successfully.')
            elif action == 'add_fee':
                _add_fee(request)
                messages.success(request, 'Fee record created successfully.')
            elif action == 'add_notice':
                _add_notice(request)
                messages.success(request, 'Notice created successfully.')
            else:
                messages.error(request, 'Unknown action.')
        except ValueError as exc:
            messages.error(request, str(exc))
        if institution_id:
            return redirect(f"{redirect('dashboard:data_hub').url}?institution_id={institution_id}")
        return redirect('dashboard:data_hub')

    institution = _selected_institution(request, strict=False)
    students = Student.objects.filter(institution=institution) if institution else Student.objects.none()
    teachers = Teacher.objects.filter(institution=institution) if institution else Teacher.objects.none()
    courses = Course.objects.filter(institute=institution).select_related('teacher') if institution else Course.objects.none()
    fees = FeePayment.objects.filter(student__institution=institution).select_related('student', 'student__user') if institution else FeePayment.objects.none()
    notices = _scoped_notices(request).order_by('-id')[:20]
    institutions = CoreInstitution.objects.all().order_by('name')

    return render(
        request,
        'dashboard/pages/data_hub.html',
        {
            'students': students,
            'teachers': teachers,
            'courses': courses,
            'fees': fees,
            'notices': notices,
            'institutions': institutions,
            'selected_institution': institution,
        },
    )


@require_POST
@login_required
def chatbot_ask(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'reply': 'Invalid request.'}, status=400)

    question = (payload.get('message') or '').strip()
    reply = _rule_based_reply(request.user, question)
    if reply:
        return JsonResponse({'reply': reply})

    ai_reply = _openai_reply(question)
    if ai_reply:
        return JsonResponse({'reply': ai_reply})

    return JsonResponse({'reply': 'I can help with attendance, next exam, assignments, and study guidance.'})


def _rule_based_reply(user, question):
    q = question.lower()
    student = getattr(user, 'student_profile', None)

    if 'attendance' in q and student:
        total = Attendance.objects.filter(student=student).count()
        present = Attendance.objects.filter(student=student, status='PRESENT').count()
        pct = round((present / total) * 100, 2) if total else 0
        return f'Your attendance is {pct}% ({present}/{total} days present).'

    if ('next exam' in q or 'exam' in q) and student:
        nxt = Exam.objects.filter(date__gte=date.today()).order_by('date').first()
        if nxt:
            return f'Your next exam is {nxt.name} on {nxt.date:%d %b %Y}.'
        return 'No upcoming exams are scheduled right now.'

    if 'assignment' in q and student:
        ass = Assignment.objects.order_by('due_date')[:5]
        if not ass:
            return 'No assignments are currently available.'
        titles = ', '.join(a.title for a in ass)
        return f'Latest assignments: {titles}.'

    if 'study' in q or 'help' in q:
        return 'Study plan: 45 min deep study, 10 min revision, 10 min quiz. Repeat for 3 cycles daily.'

    return None


def _openai_reply(question):
    if not settings.OPENAI_API_KEY:
        return None

    try:
        from openai import OpenAI

        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.responses.create(
            model='gpt-4.1-mini',
            input=f"You are an EMS tutor assistant. Answer briefly.\nQuestion: {question}",
        )
        return response.output_text
    except Exception:
        return None


def _user_preferences(user):
    stored = user.preferences or {}
    prefs = DEFAULT_PREFERENCES.copy()
    if isinstance(stored, dict):
        prefs.update(stored)
    return prefs


def _update_user_preferences(user, updates):
    prefs = _user_preferences(user)
    prefs.update(updates)
    user.preferences = prefs
    user.save(update_fields=['preferences'])
    return prefs


def _scoped_queryset(request, qs, institution_field='institution'):
    if request.user.is_superuser:
        return qs

    if not request.user.institution_id:
        return qs.none()

    return qs.filter(**{f'{institution_field}_id': request.user.institution_id})


def _scoped_notices(request):
    qs = Notice.objects.all()
    if request.user.is_superuser:
        return qs

    if not request.user.institution_id:
        return qs.none()

    return qs.filter(
        Q(created_by=request.user) | Q(created_by__institution_id=request.user.institution_id)
    ).distinct()


def _scoped_exams(request):
    qs = Exam.objects.all()
    if request.user.is_superuser:
        return qs

    if not request.user.institution_id:
        return qs.none()

    qs = qs.filter(
        examsubject__marks__student__institution_id=request.user.institution_id
    ).distinct()

    if request.user.role == 'STUDENT':
        qs = qs.filter(
            examsubject__marks__student__user=request.user
        ).distinct()

    return qs


def _selected_institution(request, strict=True):
    if request.user.is_superuser:
        institution_id = request.POST.get('institution_id') or request.GET.get('institution_id')
        if institution_id:
            return CoreInstitution.objects.filter(pk=institution_id).first()
        if strict:
            raise ValueError('Please select institution.')
        return None

    if request.user.institution:
        return request.user.institution
    if strict:
        raise ValueError('Your account has no institution mapped.')
    return None


def _build_unique_username(base):
    candidate = base
    i = 1
    while User.objects.filter(username=candidate).exists():
        i += 1
        candidate = f'{base}{i}'
    return candidate


def _add_student(request):
    institution = _selected_institution(request)
    first_name = request.POST.get('student_first_name', '').strip()
    last_name = request.POST.get('student_last_name', '').strip()
    email = request.POST.get('student_email', '').strip().lower()
    institute_id = request.POST.get('student_institute_id', '').strip()
    class_name = request.POST.get('student_class_name', '').strip()
    section = request.POST.get('student_section', '').strip()
    roll_no = request.POST.get('student_roll_no', '').strip()
    dob = request.POST.get('student_dob', '').strip()

    if not all([first_name, email, institute_id, class_name, section, roll_no, dob]):
        raise ValueError('Student form is incomplete.')
    if User.objects.filter(email__iexact=email).exists():
        raise ValueError('Student email already exists.')
    if User.objects.filter(institute_id__iexact=institute_id).exists():
        raise ValueError('Student institute ID already exists.')

    username = _build_unique_username(email.split('@')[0].lower().replace(' ', ''))
    password = datetime.strptime(dob, '%Y-%m-%d').strftime('%d%m%Y')

    with transaction.atomic():
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role='STUDENT',
            institute_id=institute_id,
            date_of_birth=dob,
            institution=institution,
        )
        user.set_password(password)
        user.save()
        Student.objects.create(
            user=user,
            institution=institution,
            roll_no=roll_no,
            class_name=class_name,
            section=section,
        )


def _add_teacher(request):
    institution = _selected_institution(request)
    first_name = request.POST.get('teacher_first_name', '').strip()
    last_name = request.POST.get('teacher_last_name', '').strip()
    email = request.POST.get('teacher_email', '').strip().lower()
    institute_id = request.POST.get('teacher_institute_id', '').strip()
    subject = request.POST.get('teacher_subject', '').strip()
    qualification = request.POST.get('teacher_qualification', '').strip()
    dob = request.POST.get('teacher_dob', '').strip()

    if not all([first_name, email, institute_id, subject, qualification, dob]):
        raise ValueError('Teacher form is incomplete.')
    if User.objects.filter(email__iexact=email).exists():
        raise ValueError('Teacher email already exists.')
    if User.objects.filter(institute_id__iexact=institute_id).exists():
        raise ValueError('Teacher institute ID already exists.')

    username = _build_unique_username(email.split('@')[0].lower().replace(' ', ''))
    password = datetime.strptime(dob, '%Y-%m-%d').strftime('%d%m%Y')

    with transaction.atomic():
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role='TEACHER',
            institute_id=institute_id,
            date_of_birth=dob,
            institution=institution,
        )
        user.set_password(password)
        user.save()
        Teacher.objects.create(
            user=user,
            institution=institution,
            subject=subject[:100],
            qualification=qualification[:100],
        )


def _add_course(request):
    institution = _selected_institution(request)
    code = request.POST.get('course_code', '').strip().upper()
    name = request.POST.get('course_name', '').strip()
    credits = request.POST.get('course_credits', '3').strip()
    teacher_id = request.POST.get('course_teacher_id', '').strip()
    description = request.POST.get('course_description', '').strip()

    if not code or not name:
        raise ValueError('Course code and name are required.')
    if Course.objects.filter(code__iexact=code).exists():
        raise ValueError('Course code already exists.')

    teacher = None
    if teacher_id:
        teacher = Teacher.objects.filter(pk=teacher_id, institution=institution).first()
        if not teacher:
            raise ValueError('Selected teacher not found for this institution.')

    Course.objects.create(
        institute=institution,
        teacher=teacher,
        code=code,
        name=name,
        credits=int(credits or 3),
        description=description,
    )


def _add_fee(request):
    institution = _selected_institution(request, strict=False)
    student_id = request.POST.get('fee_student_id', '').strip()
    amount = request.POST.get('fee_amount', '').strip()
    status = request.POST.get('fee_status', 'PENDING').strip()
    reference = request.POST.get('fee_reference', '').strip()
    payment_date = request.POST.get('fee_payment_date', '').strip() or None

    student_qs = Student.objects.filter(pk=student_id)
    if institution:
        student_qs = student_qs.filter(institution=institution)
    student = student_qs.first()
    if not student:
        raise ValueError('Valid student is required for fee record.')
    if not amount:
        raise ValueError('Fee amount is required.')

    FeePayment.objects.create(
        student=student,
        amount=amount,
        status=status,
        reference=reference,
        payment_date=payment_date,
    )


def _add_notice(request):
    title = request.POST.get('notice_title', '').strip()
    description = request.POST.get('notice_description', '').strip()
    target = request.POST.get('notice_target', 'all').strip()
    expiry_date = request.POST.get('notice_expiry_date', '').strip() or None

    if not title or not description:
        raise ValueError('Notice title and description are required.')

    # Notice model uses institutions app; keep nullable to avoid cross-app FK mismatch.
    Notice.objects.create(
        title=title,
        description=description,
        target=target,
        expiry_date=expiry_date,
        institution=None,
        created_by=request.user,
    )
