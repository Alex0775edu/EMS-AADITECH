import uuid

from django.db import models
from django.conf import settings
from students.models import Student

STATUS_CHOICES = (
    ('PRESENT', 'Present'),
    ('ABSENT', 'Absent'),
    ('LEAVE', 'Leave'),
)

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {self.status}"
    class Meta:
        unique_together = ('student', 'date')


class AttendanceSession(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    session_date = models.DateField()
    session_start = models.DateTimeField()
    session_end = models.DateTimeField(null=True, blank=True)
    qr_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Attendance {self.session_date} ({self.qr_token})"


class AttendanceScan(models.Model):
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='scans')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_scans')
    scanned_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PRESENT')

    class Meta:
        unique_together = ('session', 'student')

    def __str__(self):
        return f"{self.student.user.username} - {self.session.session_date}"
