from django.urls import path
from . import views
app_name = 'attendance'
urlpatterns = [
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('report/', views.attendance_report, name='attendance_report'),
    path('face-mark/', views.face_attendance, name='face_attendance'),
]
