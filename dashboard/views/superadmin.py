from django.shortcuts import render
from accounts.decorators import role_required

@role_required(['SUPER_ADMIN'])
def super_dashboard(request):
    return render(request, 'dashboard/super.html')
