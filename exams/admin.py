# exams/admin.py
from django.contrib import admin
from .models import Exam, ExamSubject, Marks

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
