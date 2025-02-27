from django.contrib import admin
from .models import Order, Trade

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Trade._meta.fields]