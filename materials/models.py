from django.db import models
from django.conf import settings

from dashboard.models import Course


MATERIAL_TYPES = (
    ('PDF', 'PDF'),
    ('VIDEO', 'Video'),
    ('LINK', 'External Link'),
)

ACCESS_ACTIONS = (
    ('VIEW', 'View'),
    ('DOWNLOAD', 'Download'),
)


class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=180)
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPES, default='PDF')
    file = models.FileField(upload_to='materials/', null=True, blank=True)
    url = models.URLField(blank=True)
    is_downloadable = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class MaterialAccessLog(models.Model):
    material = models.ForeignKey(CourseMaterial, on_delete=models.CASCADE, related_name='access_logs')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACCESS_ACTIONS, default='VIEW')
    accessed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.material_id} - {self.action}"
