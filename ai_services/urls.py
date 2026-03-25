from django.urls import path
from . import views

app_name = 'ai_services'

urlpatterns = [
    path('insights/', views.ai_insights, name='ai_insights'),
]
