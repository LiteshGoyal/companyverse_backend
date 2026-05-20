from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "ADMIN"
    

# BasePermission allows to use IsAdmin in the permission_classes list