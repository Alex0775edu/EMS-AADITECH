from django.contrib import admin

from .models import EventLog, DailyMetric


@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'user', 'ip_address', 'created_at')
    list_filter = ('event_type', 'created_at')
    search_fields = ('user__username', 'ip_address', 'metadata')


@admin.register(DailyMetric)
class DailyMetricAdmin(admin.ModelAdmin):
    list_display = ('metric', 'metric_date', 'institution', 'value')
    list_filter = ('metric', 'metric_date')
    search_fields = ('institution__name',)
