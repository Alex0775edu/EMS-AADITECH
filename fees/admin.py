# fees/admin.py
from django.contrib import admin
from .models import FeeStructure, FeeTransaction
@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('id',)

@admin.register(FeeTransaction)
class FeeTransactionAdmin(admin.ModelAdmin):
    list_display = ('id',)
