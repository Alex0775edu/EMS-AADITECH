from django.db import models
from django.conf import settings

from dashboard.models import Course
from students.models import Student


class AIChatSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_chat_sessions')
    context = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_active_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"AI chat {self.user.username}"


class AIRecommendation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_recommendations')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='ai_recommendations')
    score = models.FloatField(default=0)
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.course.code}"


class AIPerformanceInsight(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='ai_insights')
    insight_type = models.CharField(max_length=80)
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.insight_type}"
