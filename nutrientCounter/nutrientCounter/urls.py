from django.contrib import admin
from django.urls import path
from core import views
from custom_auth import views as auth_views
from django.contrib.auth import views as djauth_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("register/", auth_views.register, name="register"), 
    path("accounts/login/", djauth_views.LoginView.as_view(template_name="auth/login.html"), name="login"), 
    path("logout/", djauth_views.LogoutView.as_view(), name="logout"),
    path('', views.index, name="index"),
    path('delete/<int:id>/', views.delete_consume, name="delete"),
    path("add-food/", views.add_food, name="add-food"),
    path("update-goals/", views.update_goals, name="update-goals"), 
]