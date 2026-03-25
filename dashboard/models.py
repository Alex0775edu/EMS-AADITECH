from django.db import models
from django.conf import settings

from core.models import Institution
from students.models import Student
from teachers.models import Teacher


COURSE_LEVELS = (
    ('BEGINNER', 'Beginner'),
    ('INTERMEDIATE', 'Intermediate'),
    ('ADVANCED', 'Advanced'),
)

LESSON_TYPES = (
    ('VIDEO', 'Video'),
    ('PDF', 'PDF'),
    ('QUIZ', 'Quiz'),
    ('LIVE', 'Live'),
    ('TEXT', 'Text'),
)

ENROLLMENT_STATUS = (
    ('ACTIVE', 'Active'),
    ('COMPLETED', 'Completed'),
    ('DROPPED', 'Dropped'),
)

SUBMISSION_STATUS = (
    ('SUBMITTED', 'Submitted'),
    ('GRADED', 'Graded'),
    ('LATE', 'Late'),
    ('RESUBMITTED', 'Resubmitted'),
)


class Course(models.Model):
    institute = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='courses')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=40, unique=True)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=255, blank=True)
    cover_image = models.FileField(upload_to='courses/covers/', null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    language = models.CharField(max_length=40, default='English')
    level = models.CharField(max_length=20, choices=COURSE_LEVELS, default='BEGINNER')
    rating_average = models.FloatField(default=0)
    rating_count = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False)
    credits = models.PositiveSmallIntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(default=1)
    is_published = models.BooleanField(default=False)
    release_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.code} - {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=180)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPES, default='VIDEO')
    content_url = models.URLField(blank=True)
    attachment = models.FileField(upload_to='courses/lessons/', null=True, blank=True)
    duration_minutes = models.PositiveSmallIntegerField(default=0)
    order = models.PositiveSmallIntegerField(default=1)
    is_preview = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.module.course.code} - {self.title}"


class CourseEnrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='course_enrollments')
    status = models.CharField(max_length=20, choices=ENROLLMENT_STATUS, default='ACTIVE')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    progress_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        unique_together = ('course', 'student')

    def __str__(self):
        return f"{self.student} -> {self.course.code}"


class LessonProgress(models.Model):
    enrollment = models.ForeignKey(CourseEnrollment, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress_records')
    progress_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    last_position_seconds = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('enrollment', 'lesson')

    def __str__(self):
        return f"{self.enrollment} - {self.lesson.title}"


class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='course_reviews')
    rating = models.PositiveSmallIntegerField(default=5)
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'student')

    def __str__(self):
        return f"{self.course.code} - {self.rating}"


class Assignment(models.Model):
    institute = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='assignments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    attachment = models.FileField(upload_to='assignments/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assignment_submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='assignments/submissions/', null=True, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=SUBMISSION_STATUS, default='SUBMITTED')
    grade = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    plagiarism_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    graded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f"{self.assignment.title} - {self.student}"


class Announcement(models.Model):
    institute = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='announcements')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=160)
    message = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class FeePayment(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('PARTIAL', 'Partial'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fee_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_date = models.DateField(null=True, blank=True)
    reference = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.amount} ({self.status})"


class StudentPerformance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='performance_records')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='performance_records')
    score = models.FloatField(default=0)
    remarks = models.CharField(max_length=200, blank=True)
    graded_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} - {self.course} - {self.score}"


class ActivityLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.method} {self.path}"
