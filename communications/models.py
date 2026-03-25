from django.db import models
from django.conf import settings


THREAD_TYPES = (
    ('DIRECT', 'Direct'),
    ('GROUP', 'Group'),
    ('SUPPORT', 'Support'),
)

TICKET_STATUS = (
    ('OPEN', 'Open'),
    ('IN_PROGRESS', 'In Progress'),
    ('RESOLVED', 'Resolved'),
    ('CLOSED', 'Closed'),
)

TICKET_PRIORITY = (
    ('LOW', 'Low'),
    ('MEDIUM', 'Medium'),
    ('HIGH', 'High'),
)


class Thread(models.Model):
    thread_type = models.CharField(max_length=20, choices=THREAD_TYPES, default='DIRECT')
    title = models.CharField(max_length=180, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"{self.thread_type} thread {self.id}"


class ThreadParticipant(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='threads')
    is_admin = models.BooleanField(default=False)
    last_read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('thread', 'user')

    def __str__(self):
        return f"{self.thread_id} - {self.user.username}"


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    body = models.TextField()
    attachment = models.FileField(upload_to='messages/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.thread_id} - {self.sender_id}"


class SupportTicket(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=180)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=TICKET_STATUS, default='OPEN')
    priority = models.CharField(max_length=20, choices=TICKET_PRIORITY, default='MEDIUM')
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.subject} ({self.status})"


class TicketMessage(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Ticket {self.ticket_id} message"
