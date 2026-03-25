from django.urls import path

from . import views

app_name = 'fees'

urlpatterns = [
    path('structure/', views.fee_structure, name='fee_structure'),
    path('structure/add/', views.fee_structure_add, name='fee_structure_add'),
    path('structure/edit/<int:structure_id>/', views.fee_structure_edit, name='fee_structure_edit'),
    path('structure/delete/<int:structure_id>/', views.fee_structure_delete, name='fee_structure_delete'),
    path('structure/collect/<int:structure_id>/', views.fee_collect, name='fee_collect'),
    path('history/', views.fee_history, name='fee_history'),
    path('invoice/', views.fee_invoice, name='fee_invoice'),
    path('receipt/<int:transaction_id>/', views.fee_receipt, name='fee_receipt'),
]
