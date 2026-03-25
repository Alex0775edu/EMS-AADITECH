from django.contrib import admin

from .models import EventLog, DailyMetric


admin.site.register(EventLog)
admin.site.register(DailyMetric)
