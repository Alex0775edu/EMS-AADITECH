from django.db import models
from institutions.models import Institution
from accounts.models import User


class Class(models.Model):
    name = models.CharField(max_length=50)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.institution.name}"


class Section(models.Model):
    name = models.CharField(max_length=5)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.class_name.name} - {self.name}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.institution.name}"


class TeacherAssignment(models.Model):
    teacher = models.ForeignKey(User, limit_choices_to={"role": "teacher"}, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    session_start = models.DateField()
    session_end = models.DateField()

    def __str__(self):
        return f"{self.teacher.username} -> {self.class_name.name}{self.section.name} ({self.subject.name})"
