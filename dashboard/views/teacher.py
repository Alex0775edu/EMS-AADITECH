from django.shortcuts import render
from accounts.decorators import role_required

@role_required(['TEACHER'])
def teacher_dashboard(request):
    return render(request, 'dashboard/teacher.html')
