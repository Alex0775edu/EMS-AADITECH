from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('events/', views.event_list, name='event_list'),
]
