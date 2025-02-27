from django.contrib import admin
from .models import SalesOrder, Invoice, Discount

admin.site.register(SalesOrder)
admin.site.register(Invoice)
admin.site.register(Discount)
