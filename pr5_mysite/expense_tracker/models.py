from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name  
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True) 
    name = models.CharField(max_length=200)
    amount = models.IntegerField()
    description = models.TextField() 
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.amount} - {self.category.name if self.category else 'No Category'}"
    
class GroupExpense(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    users = models.ManyToManyField(User)

    def split_expense(self):
        return self.amount / self.users.count() if self.users.count() > 0 else 0

    def __str__(self):
        return f"{self.name} - {self.amount}"
