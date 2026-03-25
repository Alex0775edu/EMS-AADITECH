# documents/models.py
from django.db import models
from accounts.models import User
from institutions.models import Institution

DOCUMENT_TYPE = [
    ('id', 'ID Proof'),
    ('marksheet', 'Marksheet'),
    ('certificate', 'Certificate'),
    ('tc', 'Transfer Certificate'),
    ('other', 'Other'),
]

class Document(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.owner.username}"
