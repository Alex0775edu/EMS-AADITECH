# notices/admin.py
from django.contrib import admin
from .models import Notice

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'institution', 'target', 'publish_date', 'expiry_date')
    list_filter = ('institution', 'target', 'publish_date')
    search_fields = ('title', 'description')
