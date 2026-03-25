from datetime import date

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Exam

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
def exam_list(request):
    exams = Exam.objects.all()
    if not request.user.is_superuser:
        if request.user.institution_id:
            exams = exams.filter(
                examsubject__marks__student__institution_id=request.user.institution_id
            ).distinct()
        else:
            exams = exams.none()
    status = request.GET.get('status', '').strip()
    today = date.today()
    if status == 'upcoming':
        exams = exams.filter(date__gte=today)
    elif status == 'past':
        exams = exams.filter(date__lt=today)
    return render(request, 'exams/exam_list.html', {'exams': exams.order_by('date'), 'today': today})

@login_required
def exam_add(request):
    if request.user.role == 'STUDENT':
        messages.error(request, 'Students are not allowed to create exams.')
        return redirect('exams:exam_list')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        exam_date = request.POST.get('date', '').strip()
        total_marks = request.POST.get('total_marks', '').strip()
        if not name or not exam_date or not total_marks:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('exams:exam_add')
        Exam.objects.create(name=name, date=exam_date, total_marks=total_marks)
        return redirect('exams:exam_list')
    return render(request, 'exams/exam_add.html')


@login_required
def exam_detail(request, exam_id):
    return _placeholder(
        request,
        'Exam Details',
        'Detailed exam views are coming soon.',
        back_url='/exams/',
    )


@login_required
def exam_edit(request, exam_id):
    return _placeholder(
        request,
        'Edit Exam',
        'Exam editing will be enabled in the next release.',
        back_url='/exams/',
    )


@login_required
def exam_marks(request, exam_id):
    return _placeholder(
        request,
        'Exam Marks',
        'Marks entry and analytics are coming soon.',
        back_url='/exams/',
    )
