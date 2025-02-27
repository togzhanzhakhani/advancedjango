from rest_framework.permissions import BasePermission

class IsAdminOrTrader(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'trader']

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.owner == request.user 
    
class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
    
class IsSales(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'sales'
    
class IsTrader(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'trader'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
