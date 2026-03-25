from django.db import models
from accounts.models import User
from core.models import Institution

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='student_profile')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE,related_name='students')
    roll_no = models.CharField(max_length=20)
    class_name = models.CharField(max_length=50)
    section = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.user.username} - {self.roll_no}"
