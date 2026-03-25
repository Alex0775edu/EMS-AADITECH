from django.db import models
from django.utils import timezone


class Institution(models.Model):
    name = models.CharField(max_length=255)
    type_choices = (
        ('SCHOOL', 'School'),
        ('COLLEGE', 'College'),
        ('UNIVERSITY', 'University'),
        ('COACHING', 'Coaching'),
    )
    type = models.CharField(max_length=20, choices=type_choices, default='SCHOOL')
    address = models.TextField()
    admin_email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    logo = models.ImageField(upload_to='institutions/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.type})"


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
