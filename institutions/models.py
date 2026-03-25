from django.db import models

class Institution(models.Model):
    INSTITUTE_TYPES = [
        ('school', 'School'),
        ('college', 'College'),
        ('coaching', 'Coaching'),
    ]
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=INSTITUTE_TYPES)
    address = models.TextField()
    session_start = models.DateField()
    session_end = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

