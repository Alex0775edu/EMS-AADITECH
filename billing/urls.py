from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('plans/', views.plan_list, name='plan_list'),
    path('invoices/', views.invoice_list, name='invoice_list'),
]
