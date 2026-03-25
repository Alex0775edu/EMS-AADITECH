from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from .models import Attendance
from students.models import Student
from .face_recognition_service import mark_attendance_from_face


@login_required
def mark_attendance(request):
    if request.user.role == 'STUDENT':
        messages.error(request, 'Students are not allowed to mark attendance.')
        return redirect('attendance:attendance_report')

    students = Student.objects.select_related('user')
    if getattr(request.user, 'institution_id', None):
        students = students.filter(institution_id=request.user.institution_id)

    if request.method == 'POST':
        marked = 0
        for student in students:
            status = request.POST.get(f'attendance_{student.id}')
            if status in {'PRESENT', 'ABSENT', 'LEAVE'}:
                Attendance.objects.update_or_create(
                    student=student,
                    date=timezone.now().date(),
                    defaults={'status': status},
                )
                marked += 1

        if marked:
            messages.success(request, f'Attendance saved for {marked} students.')
        else:
            messages.warning(request, 'No attendance status selected.')
        return redirect('attendance:attendance_report')

    return render(request, 'attendance/mark_attendance.html', {'students': students})


@login_required
def attendance_report(request):
    records = Attendance.objects.select_related('student', 'student__user').order_by('-date', 'student__user__first_name')
    if getattr(request.user, 'institution_id', None):
        records = records.filter(student__institution_id=request.user.institution_id)
    if request.user.role == 'STUDENT':
        records = records.filter(student__user=request.user)

    summary_qs = records.values('status').annotate(count=Count('id'))
    summary_map = {row['status']: row['count'] for row in summary_qs}
    total = sum(summary_map.values()) or 0

    summary = [
        {'label': 'Present', 'count': summary_map.get('PRESENT', 0), 'class': 'success'},
        {'label': 'Absent', 'count': summary_map.get('ABSENT', 0), 'class': 'danger'},
        {'label': 'Leave', 'count': summary_map.get('LEAVE', 0), 'class': 'warning'},
    ]
    for item in summary:
        item['pct'] = round((item['count'] / total) * 100, 1) if total else 0

    return render(
        request,
        'attendance/attendance_report.html',
        {
            'records': records[:200],
            'summary': summary,
            'total_records': total,
        },
    )


@login_required
def face_attendance(request):
    if request.user.role == 'STUDENT':
        messages.error(request, 'Students are not allowed to use face attendance marking.')
        return redirect('attendance:attendance_report')

    if request.method == 'POST':
        image = request.FILES.get('face_image')
        if not image:
            messages.error(request, 'Please upload a face image.')
            return redirect('attendance:face_attendance')

        result = mark_attendance_from_face(image)
        if result.get('success'):
            messages.success(request, result.get('message'))
        else:
            messages.error(request, result.get('message'))
        return redirect('attendance:attendance_report')

    return render(request, 'attendance/face_attendance.html')
