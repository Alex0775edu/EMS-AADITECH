from django.contrib import admin

from .models import Plan, Subscription, Coupon, Invoice, PaymentRecord


admin.site.register(Plan)
admin.site.register(Subscription)
admin.site.register(Coupon)
admin.site.register(Invoice)
admin.site.register(PaymentRecord)
