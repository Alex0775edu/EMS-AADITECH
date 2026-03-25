from django.contrib import admin

from .models import CourseMaterial, MaterialAccessLog


admin.site.register(CourseMaterial)
admin.site.register(MaterialAccessLog)
