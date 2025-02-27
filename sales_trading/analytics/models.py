from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TradeReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_trading_volume = models.DecimalField(max_digits=15, decimal_places=2)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    profit_loss = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"Report {self.id} - {self.user.username}"
