from django.db import models
from django.conf import settings

class SalesOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('processed', 'Processed'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sales_orders')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"


class Invoice(models.Model):
    order = models.OneToOneField(SalesOrder, on_delete=models.CASCADE, related_name='invoice')
    pdf_file = models.FileField(upload_to='invoices/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice for Order {self.order.id}"


class Discount(models.Model):
    code = models.CharField(max_length=20, unique=True)
    percentage = models.FloatField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Discount {self.code} - {self.percentage}%"
