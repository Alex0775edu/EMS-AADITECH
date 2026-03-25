from django.db import models
from accounts.models import User
from core.models import Institution


class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        null=True,
        blank=True,
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name='teachers',
        null=True,
        blank=True,
    )
    subject = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return f"{self.name} ({self.subject})"

    @property
    def name(self):
        if self.user_id:
            full_name = f"{self.user.first_name} {self.user.last_name}".strip()
            return full_name or self.user.username
        return "Unknown Teacher"
