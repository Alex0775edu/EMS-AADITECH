from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Plan, Invoice


@login_required
def plan_list(request):
    plans = Plan.objects.filter(is_active=True).order_by('price')
    return render(request, 'billing/plans.html', {'plans': plans})


@login_required
def invoice_list(request):
    invoices = Invoice.objects.order_by('-issued_at')[:20]
    return render(request, 'billing/invoices.html', {'invoices': invoices})
