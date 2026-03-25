from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
        ('INSTITUTE', 'Institute'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    institute_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    institution = models.ForeignKey(
        'core.Institution',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
    )
    mfa_enabled = models.BooleanField(default=False)
    consent_opt_in = models.BooleanField(default=True)
    preferences = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.username

    def default_password_from_dob(self):
        if not self.date_of_birth:
            return None
        return self.date_of_birth.strftime('%d%m%Y')
