from django.db import models
from django.conf import settings

from core.models import Institution


class EventLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    event_type = models.CharField(max_length=120)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} - {self.created_at:%Y-%m-%d}"


class DailyMetric(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, blank=True)
    metric = models.CharField(max_length=120)
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    metric_date = models.DateField()

    class Meta:
        unique_together = ('institution', 'metric', 'metric_date')

    def __str__(self):
        return f"{self.metric} - {self.metric_date}"
