from django.contrib import admin
from .models import (
    ActivityLog,
    Announcement,
    Assignment,
    Course,
    FeePayment,
    StudentPerformance,
)

admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(Announcement)
admin.site.register(FeePayment)
admin.site.register(StudentPerformance)
admin.site.register(ActivityLog)
