from rest_framework.permissions import BasePermission

class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ["ADMIN","MANAGER"]
    
class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.role not in ["ADMIN","MANAGER"]
    

# BasePermission allows to use IsAdmin in the permission_classes list

class IsRequirementOwnerCompany(BasePermission):

    def has_object_permission(self, request, view, obj):

        if hasattr(obj, "requirement"):
            return obj.requirement.company == request.user.company

        return obj.company == request.user.company