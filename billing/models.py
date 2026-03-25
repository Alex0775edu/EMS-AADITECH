from django.db import models
from django.conf import settings

from core.models import Institution


PLAN_INTERVALS = (
    ('MONTH', 'Monthly'),
    ('YEAR', 'Yearly'),
)

SUBSCRIPTION_STATUS = (
    ('ACTIVE', 'Active'),
    ('PAST_DUE', 'Past Due'),
    ('CANCELED', 'Canceled'),
)

COUPON_TYPE = (
    ('PERCENT', 'Percent'),
    ('AMOUNT', 'Amount'),
)

INVOICE_STATUS = (
    ('DRAFT', 'Draft'),
    ('ISSUED', 'Issued'),
    ('PAID', 'Paid'),
    ('OVERDUE', 'Overdue'),
)


class Plan(models.Model):
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    interval = models.CharField(max_length=10, choices=PLAN_INTERVALS, default='MONTH')
    is_active = models.BooleanField(default=True)
    features = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.name} ({self.interval})"


class Subscription(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=SUBSCRIPTION_STATUS, default='ACTIVE')
    started_at = models.DateTimeField(auto_now_add=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.institution.name} - {self.plan}"


class Coupon(models.Model):
    code = models.CharField(max_length=40, unique=True)
    discount_type = models.CharField(max_length=10, choices=COUPON_TYPE, default='PERCENT')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    usage_limit = models.PositiveIntegerField(default=0)
    times_used = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.code


class Invoice(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='invoices')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    status = models.CharField(max_length=20, choices=INVOICE_STATUS, default='DRAFT')
    issued_at = models.DateTimeField(auto_now_add=True)
    due_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Invoice {self.id} - {self.status}"


class PaymentRecord(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    provider = models.CharField(max_length=50, default='manual')
    provider_reference = models.CharField(max_length=120, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.provider} - {self.amount}"
