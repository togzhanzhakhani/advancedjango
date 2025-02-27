from django.db import models
from django.conf import settings

class Order(models.Model):
    ORDER_TYPES = (
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    )

    ORDER_STATUS = (
        ('PENDING', 'Pending'),
        ('PARTIALLY_FILLED', 'Partially Filled'),
        ('FILLED', 'Filled'),
        ('CANCELED', 'Canceled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    order_type = models.CharField(max_length=4, choices=ORDER_TYPES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)  
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.order_type} {self.quantity} @ {self.price}"


class Trade(models.Model):
    buy_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='buy_trades')
    sell_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='sell_trades')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trade {self.quantity} @ {self.price}"


class OrderBook(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="order_book")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OrderBook {self.order}"
