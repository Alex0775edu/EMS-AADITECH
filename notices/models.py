# notices/models.py
from django.db import models
from institutions.models import Institution
from accounts.models import User

TARGET_CHOICES = [
    ('all', 'All'),
    ('students', 'Students'),
    ('teachers', 'Teachers'),
    ('staff', 'Staff'),
]

class Notice(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    target = models.CharField(max_length=20, choices=TARGET_CHOICES, default='all')
    publish_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        institution_name = self.institution.name if self.institution else 'General'
        return f"{self.title} ({institution_name})"
