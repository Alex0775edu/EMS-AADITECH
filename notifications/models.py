# notifications/models.py
from django.db import models
from accounts.models import User
from institutions.models import Institution

NOTIFICATION_TYPE = [
    ('inapp', 'In-App'),
    ('email', 'Email'),
    ('sms', 'SMS'),
]

NOTIFICATION_STATUS = [
    ('sent', 'Sent'),
    ('pending', 'Pending'),
    ('failed', 'Failed'),
]

class Notification(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPE, default='inapp')
    target_users = models.ManyToManyField(User)
    status = models.CharField(max_length=10, choices=NOTIFICATION_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.notification_type})"


class DeviceToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='device_tokens')
    token = models.CharField(max_length=255, unique=True)
    platform = models.CharField(max_length=30, default='web')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.platform}"


class PushNotification(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    recipients = models.ManyToManyField(DeviceToken, related_name='push_notifications')
    status = models.CharField(max_length=10, choices=NOTIFICATION_STATUS, default='pending')

    def __str__(self):
        return f"{self.title} ({self.status})"
