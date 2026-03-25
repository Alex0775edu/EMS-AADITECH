from accounts.models import User
from attendance.models import Attendance
from fees.models import FeeTransaction
from exams.models import Marks

def student_attendance_percentage(student):
    total = Attendance.objects.filter(student=student).count()
    present = Attendance.objects.filter(student=student, status='present').count()
    return round((present / total) * 100, 2) if total > 0 else 0


def student_result_summary(student):
    records = Marks.objects.filter(student=student)
    total = sum([r.marks_obtained for r in records])
    count = records.count()
    percentage = (total / count) if count else 0
    return {
        "subjects": records,
        "total": total,
        "percentage": round(percentage, 2)
    }



def student_fee_status(student):
    paid = FeeTransaction.objects.filter(student=student, status='paid').count()
    pending = FeeTransaction.objects.filter(student=student, status='pending').count()
    return {
        "paid": paid,
        "pending": pending
    }

def institution_dashboard(institution):
    students = User.objects.filter(role='student', institution=institution).count()
    teachers = User.objects.filter(role='teacher', institution=institution).count()
    attendance = Attendance.objects.filter(student__institution=institution).count()
    fees_paid = FeeTransaction.objects.filter(student__institution=institution, status='paid').count()

    return {
        "students": students,
        "teachers": teachers,
        "attendance_records": attendance,
        "fees_paid": fees_paid
    }
