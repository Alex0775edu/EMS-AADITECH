from django.db import models
from django.conf import settings
from students.models import Student


class Exam(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    total_marks = models.IntegerField()

    def __str__(self):
        return self.name

class ExamSubject(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.exam.name} - {self.subject}"


class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam_subject = models.ForeignKey(ExamSubject, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField()

    def __str__(self):
        return f"{self.exam_subject.exam.name} - {self.student.user.username}"


QUESTION_TYPES = (
    ('MCQ', 'Multiple Choice'),
    ('TRUE_FALSE', 'True/False'),
    ('SHORT', 'Short Answer'),
)


class QuestionBank(models.Model):
    title = models.CharField(max_length=160)
    subject = models.CharField(max_length=120, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    bank = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='MCQ')
    prompt = models.TextField()
    options = models.JSONField(default=list, blank=True)
    correct_answer = models.CharField(max_length=255, blank=True)
    marks = models.PositiveSmallIntegerField(default=1)
    explanation = models.TextField(blank=True)

    def __str__(self):
        return f"{self.bank.title} - {self.prompt[:40]}"


class OnlineExam(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='online_sessions')
    bank = models.ForeignKey(QuestionBank, on_delete=models.SET_NULL, null=True, blank=True)
    duration_minutes = models.PositiveSmallIntegerField(default=30)
    total_questions = models.PositiveSmallIntegerField(default=10)
    is_published = models.BooleanField(default=False)
    allow_negative = models.BooleanField(default=False)

    def __str__(self):
        return f"Online {self.exam.name}"


class ExamAttempt(models.Model):
    online_exam = models.ForeignKey(OnlineExam, on_delete=models.CASCADE, related_name='attempts')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(default=0)
    status = models.CharField(max_length=20, default='IN_PROGRESS')

    class Meta:
        unique_together = ('online_exam', 'student')

    def __str__(self):
        return f"{self.student.user.username} - {self.online_exam.exam.name}"


class ExamAnswer(models.Model):
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    selected_answer = models.CharField(max_length=255, blank=True)
    is_correct = models.BooleanField(default=False)
    marks_awarded = models.FloatField(default=0)

    class Meta:
        unique_together = ('attempt', 'question')

    def __str__(self):
        return f"{self.attempt} - {self.question.id}"
