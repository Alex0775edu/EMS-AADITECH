from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('add/', views.student_add, name='student_add'),
    path('detail/<int:student_id>/', views.student_detail, name='student_detail'),
    path('edit/<int:student_id>/', views.student_edit, name='student_edit'),
    path('attendance/<int:student_id>/', views.student_attendance, name='student_attendance'),
]
