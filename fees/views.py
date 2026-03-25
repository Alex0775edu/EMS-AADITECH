from datetime import date

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum

from students.models import Student
from .models import Fee, FeeTransaction

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
def fee_structure(request):
    fees = Fee.objects.select_related('student', 'student__user')
    if not request.user.is_superuser:
        fees = fees.filter(student__institution_id=request.user.institution_id)
    total_collected = fees.filter(paid=True).aggregate(total=Sum('amount')).get('total') or 0
    total_pending = fees.filter(paid=False).aggregate(total=Sum('amount')).get('total') or 0
    total_overdue = fees.filter(paid=False, due_date__lt=date.today()).aggregate(total=Sum('amount')).get('total') or 0

    students = Student.objects.select_related('user')
    if not request.user.is_superuser:
        students = students.filter(institution_id=request.user.institution_id)

    return render(
        request,
        'fees/fee_structure.html',
        {
            'fees': fees.order_by('-due_date'),
            'total_collected': total_collected,
            'total_pending': total_pending,
            'total_overdue': total_overdue,
            'students': students,
        },
    )

@login_required
def fee_history(request):
    transactions = FeeTransaction.objects.select_related('student', 'student__user')
    if not request.user.is_superuser:
        transactions = transactions.filter(student__institution_id=request.user.institution_id)
    total_credit = transactions.filter(transaction_type='CREDIT').aggregate(total=Sum('amount')).get('total') or 0
    total_debit = transactions.filter(transaction_type='DEBIT').aggregate(total=Sum('amount')).get('total') or 0
    balance = total_credit - total_debit
    return render(
        request,
        'fees/fee_history.html',
        {
            'transactions': transactions.order_by('-transaction_date'),
            'total_credit': total_credit,
            'total_debit': total_debit,
            'balance': balance,
        },
    )


@login_required
def fee_structure_add(request):
    if request.method != 'POST':
        return redirect('fees:fee_structure')
    if request.user.role == 'STUDENT':
        messages.error(request, 'Students are not allowed to add fee records.')
        return redirect('fees:fee_structure')

    student_id = request.POST.get('student_id')
    amount = request.POST.get('amount')
    due_date = request.POST.get('due_date')

    student = Student.objects.filter(pk=student_id).first()
    if not student:
        messages.error(request, 'Please select a valid student.')
        return redirect('fees:fee_structure')

    if not amount or not due_date:
        messages.error(request, 'Amount and due date are required.')
        return redirect('fees:fee_structure')

    Fee.objects.create(
        student=student,
        amount=amount,
        due_date=due_date,
        paid=False,
    )
    messages.success(request, 'Fee record created successfully.')
    return redirect('fees:fee_structure')


@login_required
def fee_structure_edit(request, structure_id):
    return _placeholder(
        request,
        'Edit Fee Structure',
        'Fee structure editing will be available soon.',
        back_url='/fees/structure/',
    )


@login_required
def fee_structure_delete(request, structure_id):
    return _placeholder(
        request,
        'Delete Fee Structure',
        'Fee deletion workflow will be enabled shortly.',
        back_url='/fees/structure/',
    )


@login_required
def fee_collect(request, structure_id):
    if request.user.role == 'STUDENT':
        messages.error(request, 'Students are not allowed to collect fees.')
        return redirect('fees:fee_structure')
    fee = Fee.objects.filter(pk=structure_id).first()
    if not fee:
        messages.error(request, 'Fee record not found.')
        return redirect('fees:fee_structure')

    if not fee.paid:
        fee.paid = True
        fee.save(update_fields=['paid'])
        FeeTransaction.objects.create(
            student=fee.student,
            amount=fee.amount,
            transaction_type='CREDIT',
            description=f'Fee payment for {fee.student.roll_no}',
        )
        messages.success(request, 'Fee marked as paid.')
    else:
        messages.info(request, 'Fee is already marked as paid.')
    return redirect('fees:fee_structure')


@login_required
def fee_invoice(request):
    return _placeholder(
        request,
        'Fee Invoice',
        'Invoice generation will be available soon.',
        back_url='/fees/history/',
    )


@login_required
def fee_receipt(request, transaction_id):
    return _placeholder(
        request,
        'Fee Receipt',
        'Receipt generation will be available soon.',
        back_url='/fees/history/',
    )
