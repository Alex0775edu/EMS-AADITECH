from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import CourseMaterial


@login_required
def material_library(request):
    materials = CourseMaterial.objects.order_by('-uploaded_at')[:30]
    return render(request, 'materials/library.html', {'materials': materials})
