# classes/admin.py
from django.contrib import admin
from .models import Class, Section, Subject, TeacherAssignment

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution')
    list_filter = ('institution',)
    search_fields = ('name',)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_name')
    list_filter = ('class_name__institution',)
    search_fields = ('name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution')
    list_filter = ('institution',)
    search_fields = ('name',)

@admin.register(TeacherAssignment)
class TeacherAssignmentAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'class_name', 'section', 'subject', 'session_start', 'session_end')
    list_filter = ('class_name__institution', 'subject', 'teacher')
    search_fields = ('teacher__username', 'class_name__name', 'section__name', 'subject__name')