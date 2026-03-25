from django.urls import path
from . import views

app_name = 'communications'

urlpatterns = [
    path('threads/', views.thread_list, name='thread_list'),
    path('tickets/', views.ticket_list, name='ticket_list'),
]
