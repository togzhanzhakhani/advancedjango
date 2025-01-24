from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email, first_name, last_name, password, role='admin')
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Project(models.Model): 
    name = models.CharField(max_length=100) 
    description = models.TextField() 
    start_date = models.DateField() 
    end_date = models.DateField() 

    def __str__(self): 

        return self.name 

class Category(models.Model): 
    name = models.CharField(max_length=100) 

    def __str__(self): 

        return self.name 

class Priority(models.Model): 
    level = models.CharField(max_length=50)  

    def __str__(self): 

        return self.level 

class Task(models.Model): 
    title = models.CharField(max_length=200) 
    description = models.TextField() 
    project = models.ForeignKey(Project, on_delete=models.CASCADE) 
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True) 
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True) 
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) 
    due_date = models.DateField() 

    def __str__(self): 

        return self.title