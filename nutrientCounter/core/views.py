from django.shortcuts import render,redirect
from .models import Food, Consume, HealthGoal
from django.contrib.auth.decorators import login_required
from .forms import FoodForm, HealthGoalForm

@login_required
def index(request):
    if request.method =="POST":
        food_consumed = request.POST['food_consumed']
        consume = Food.objects.get(name=food_consumed)
        user = request.user 
        consume = Consume(user=user, food_consumed=consume)
        consume.save()
        foods = Food.objects.all()        
    else: 
        health_goal, _ = HealthGoal.objects.get_or_create(user=request.user)
        foods = Food.objects.all()
    consumed_food=Consume.objects.filter(user=request.user)    
    return render(request, 'core/index.html', {'foods':foods, 'consumed_food':consumed_food, "health_goal": health_goal})

def delete_consume(request, id):
    consumed_food = Consume.objects.get(id=id)
    if request.method == 'POST':
        consumed_food.delete()
        return redirect('/')
    return render(request, 'core/delete.html')

def add_food(request): 
    if request.method == "POST": 
        form = FoodForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            return redirect("index")
    else: 
        form = FoodForm() 
    return render(request, "core/add_food.html", {"form": form}) 

@login_required 
def update_goals(request): 
    goal, created = HealthGoal.objects.get_or_create(user=request.user) 
    if request.method == "POST": 
        form = HealthGoalForm(request.POST, instance=goal) 
        if form.is_valid(): 
            form.save() 
            return redirect("index") 
    else: 
        form = HealthGoalForm(instance=goal) 
    return render(request, "core/update_goals.html", {"form": form}) 