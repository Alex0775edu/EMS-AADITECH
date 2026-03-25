from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    path('', views.exam_list, name='exam_list'),
    path('add/', views.exam_add, name='exam_add'),
    path('detail/<int:exam_id>/', views.exam_detail, name='exam_detail'),
    path('edit/<int:exam_id>/', views.exam_edit, name='exam_edit'),
    path('marks/<int:exam_id>/', views.exam_marks, name='exam_marks'),
]
