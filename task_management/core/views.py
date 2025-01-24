from rest_framework.viewsets import ModelViewSet 
from .models import User, Project, Category, Priority, Task 
from .serializers import UserSerializer, ProjectSerializer, CategorySerializer, PrioritySerializer, TaskSerializer 
from rest_framework.filters import SearchFilter 
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin, IsManager, IsEmployee
from django.shortcuts import render
import logging 
logger = logging.getLogger(__name__) 

def index(request):
    return render(request, 'index.html')

class UserViewSet(ModelViewSet): 
    queryset = User.objects.all() 
    serializer_class = UserSerializer 
    permission_classes = [IsAdmin]

class ProjectViewSet(ModelViewSet): 
    permission_classes = [IsManager]
    queryset = Project.objects.all() 
    serializer_class = ProjectSerializer 

class CategoryViewSet(ModelViewSet): 
    permission_classes = [IsAuthenticated] 
    queryset = Category.objects.all() 
    serializer_class = CategorySerializer 

class PriorityViewSet(ModelViewSet): 
    permission_classes = [IsAuthenticated] 
    queryset = Priority.objects.all() 
    serializer_class = PrioritySerializer 

class TaskViewSet(ModelViewSet): 
    permission_classes = [IsEmployee]
    queryset = Task.objects.all() 
    serializer_class = TaskSerializer 
    filter_backends = [DjangoFilterBackend, SearchFilter] 
    filterset_fields = ['project', 'priority', 'category'] 
    search_fields = ['title', 'description']
    
    def perform_create(self, serializer): 
        logger.info("Creating a new task") 
        serializer.save()