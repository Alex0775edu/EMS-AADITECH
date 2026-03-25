from django.db import models
from students.models import Student

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.username} - {self.amount} - {'Paid' if self.paid else 'Pending'}"

class FeeStructure(models.Model):
    institution = models.ForeignKey('core.Institution', on_delete=models.CASCADE)
    class_name = models.CharField(max_length=50)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.institution.name} - {self.class_name} - {self.total_fee}"   
    
class FeeTransaction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    transaction_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=[('CREDIT', 'Credit'), ('DEBIT', 'Debit')])
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.transaction_type} - {self.amount} on {self.transaction_date}"     
