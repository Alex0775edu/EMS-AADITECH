from django.shortcuts import render
from accounts.decorators import role_required

@role_required(['STUDENT'])
def student_dashboard(request):
    return render(request, 'dashboard/student.html')
