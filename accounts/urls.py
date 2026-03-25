from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('register/', views.custom_register, name='register'),
    path('logout/', views.custom_logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
]
