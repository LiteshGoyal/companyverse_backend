from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import CompanySerializer, EmployeeListSerializer,EmployeeDetailSerializer
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from .permissions import IsAdmin
from auditlogs.models import AuditLog
from companymultiverse.permissions import IsAdminOrManager

from notifications.models import Notification
# Create your views here.



class CreateCompanyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        if request.user.company:
            return Response(
                {
                    "error":"User already belongs to a company"
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        serializer = CompanySerializer(data=request.data)

        if serializer.is_valid():
            company = serializer.save(owner=request.user)
            request.user.company = company
            request.user.role = "ADMIN"
            request.user.save()

            return Response({
                "message":"Company Created Successfully"
            },
            status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )
    
class AddEmployeeView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        
        email = request.data.get("email")
        role = request.data.get("role")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                "error":"User not Found"
            },
            status = status.HTTP_404_NOT_FOUND
            )

        if user.company:
            return Response({
                "error":"User already belongs to a company"
            },
            status = status.HTTP_400_BAD_REQUEST
            )
        
        user.company = request.user.company
        user.role = role
        user.save()
        Notification.objects.create(

            recipient=user,

            title="Added To Company",

            message=
            f"You were added to "
            f"{request.user.company.name}"
        )
  
# AUDIT LOG OBJECT CREATION
        AuditLog.objects.create(
            company = request.user.company,
            actor = request.user,
            action = "ASSIGN",
            entity_type = "User",
            entity_id=user.id,
            description=f"{request.user.username} added {user.username} as {user.role}"
        )
        return Response({
            "message":"Employee Added Successfully"
        },
        status = status.HTTP_200_OK
        )
    

class CompanyEmployeesView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    def get(self, request):
        
        
        employees = User.objects.filter(
            company=request.user.company
        )
        serializer = EmployeeListSerializer(employees, many=True)

        return Response(serializer.data)
    

class EmployeeDetailView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrManager
    ]

    def get(self, request, pk):

        try:

            employee = User.objects.get(
                pk=pk,
                company=request.user.company
            )

        except User.DoesNotExist:

            return Response(
                {
                    "error": "Employee not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EmployeeDetailSerializer(employee)

        return Response(serializer.data)
    
    
class UpdateEmployeeRoleView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def patch(self, request, pk):

        try:

            employee = User.objects.get(
                pk=pk,
                company=request.user.company
            )

        except User.DoesNotExist:

            return Response(
                {
                    "error": "Employee not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if employee == request.user:

            return Response(
                {
                    "error":
                    "You cannot change your own role"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        role = request.data.get("role")

        employee.role = role

        employee.save()

        return Response(
            {
                "message":
                "Role updated successfully"
            },
            status=status.HTTP_200_OK
        )
        
        

class RemoveEmployeeView(APIView):
    permission_classes=[IsAuthenticated, IsAdmin]
    
    def patch(self, request, pk):
        try:
            employee = User.objects.get(
                pk=pk,
                company = request.user.company
            )
            
        except User.DoesNotExist:
            return Response({
                "error": "Employee Not Found"
            },
                            status = status.HTTP_404_NOT_FOUND
            )
        
        if employee==request.user:
            return Response({
                "error" : "You cannot remove Yourself"
            },
                            status = status.HTTP_400_BAD_REQUEST
                            )
            
        employee.company = None
        employee.role = None
        employee.save()
        
        AuditLog.objects.create(
            company = request.user.company,
            actor = request.user,
            action = "REMOVE",
            entity_type = "USER",
            entity_id = str(employee.id),
            description = f"{request.user.username} removed"
            f"{employee.username} from company"
        )
        
        return Response({
            "message":"Employee Removed Successfully"
        },
                        status = status.HTTP_200_OK
                        )