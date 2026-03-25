# documents/admin.py
from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'document_type', 'institution', 'is_verified', 'uploaded_at')
    list_filter = ('document_type', 'institution', 'is_verified')
    search_fields = ('title', 'owner__username')
