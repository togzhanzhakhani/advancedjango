from django.shortcuts import render, redirect
from .forms import ExpenseForm
from .models import Expense, Category, GroupExpense
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import datetime
from .filters import ExpenseFilter
from django.utils import timezone

@login_required
def index(request):
    if request.method == "POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense_instance = expense.save(commit=False)
            expense_instance.user = request.user  
            expense_instance.save()
        
    expenses = Expense.objects.filter(user=request.user)
    expense_filter = ExpenseFilter(request.GET, queryset=expenses)

    total_expenses = expenses.aggregate(Sum('amount'))
    
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    yearly_sum = Expense.objects.filter(user=request.user, date__gt=last_year).aggregate(Sum('amount'))

    last_month = datetime.date.today() - datetime.timedelta(days=30)
    monthly_sum = Expense.objects.filter(user=request.user, date__gt=last_month).aggregate(Sum('amount'))

    last_week = datetime.date.today() - datetime.timedelta(days=7)
    weekly_sum = Expense.objects.filter(user=request.user, date__gt=last_week).aggregate(Sum('amount'))

    daily_sums = Expense.objects.filter(user=request.user).values('date').order_by('date').annotate(sum=Sum('amount'))
    categorical_sums = Expense.objects.filter(user=request.user).values('category').order_by('category').annotate(sum=Sum('amount'))
    
    expense_form = ExpenseForm()
    return render(request, 'expense_tracker/index.html', 
                  {'expense_form': expense_form, 
                   'expenses': expenses, 'total_expenses': total_expenses, 
                   'yearly_sum': yearly_sum, 'monthly_sum': monthly_sum, 
                   'weekly_sum': weekly_sum, 'daily_sums': daily_sums,
                   'categorical_sums': categorical_sums, 'filter': expense_filter})

@login_required
def edit(request, id):
    expense = Expense.objects.get(id=id, user=request.user) 
    expense_form = ExpenseForm(instance=expense)
    
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'expense_tracker/edit.html', {'expense_form': expense_form})

@login_required
def delete(request, id):
    if request.method == "POST" and 'delete' in request.POST:
        expense = Expense.objects.get(id=id, user=request.user)
        expense.delete()
    return redirect('index')

@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        Category.objects.create(name=name, user=request.user)
        return redirect('category_list') 
    return render(request, 'expense_tracker/add_category.html') 

@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'expense_tracker/category_list.html', {'categories': categories})

@login_required
def add_group_expense(request):
    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        users = request.POST.getlist('users')
        group_expense = GroupExpense.objects.create(
            name=name,
            amount=amount,
            date=timezone.now()
        )
        group_expense.users.set(users)  
        return redirect('group_expense_list')  
    return render(request, 'expense_tracker/add_group_expense.html')

@login_required
def group_expense_list(request):
    expenses = GroupExpense.objects.all()
    expense_shares = []
    for expense in expenses:
        shares = {}
        split = expense.split_expense()  
        for user in expense.users.all():
            shares[user.username] = split
        expense_shares.append({
            'expense': expense,
            'shares': shares
        })

    return render(request, 'expense_tracker/group_expense_list.html', {'expense_shares': expense_shares})
