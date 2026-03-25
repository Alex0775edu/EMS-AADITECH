from django.urls import path

from . import views

app_name = 'teachers'

urlpatterns = [
    path('', views.teacher_list, name='teacher_list'),
    path('add/', views.teacher_add, name='teacher_add'),
    path('detail/<int:teacher_id>/', views.teacher_detail, name='teacher_detail'),
    path('edit/<int:teacher_id>/', views.teacher_edit, name='teacher_edit'),
    path('schedule/<int:teacher_id>/', views.teacher_schedule, name='teacher_schedule'),
]
