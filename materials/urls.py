from django.urls import path
from . import views

app_name = 'materials'

urlpatterns = [
    path('library/', views.material_library, name='material_library'),
]
