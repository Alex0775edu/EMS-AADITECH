from django.shortcuts import render
from accounts.decorators import role_required

@role_required(['INSTITUTION_ADMIN'])
def institution_dashboard(request):
    return render(request, 'dashboard/institution.html')
