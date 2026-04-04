from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.summary, name='summary'),
    path('summary/', views.summary, name='summary'),
    path('events/', views.event_list, name='event_list'),
]
