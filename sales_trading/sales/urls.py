from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalesOrderViewSet, InvoiceViewSet, DiscountViewSet

router = DefaultRouter()
router.register(r'sales-orders', SalesOrderViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'discounts', DiscountViewSet)

urlpatterns = [
    path('', include(router.urls)),
]