from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer,  RegisterSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin
from django.contrib.auth import get_user_model 
from rest_framework import generics 
from rest_framework.response import Response
from rest_framework.views import APIView


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

User = get_user_model() 
 
class RegisterView(generics.CreateAPIView): 
    queryset = User.objects.all() 
    serializer_class = RegisterSerializer 

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)