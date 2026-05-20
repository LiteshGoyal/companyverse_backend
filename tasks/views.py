from django.shortcuts import render
from .serializers import TaskSerializer, UpdateTaskStatusSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import User
from rest_framework import status
from .models import Tasks
from notifications.models import Notification

from auditlogs.models import AuditLog
from companymultiverse.permissions import IsAdminOrManager

# Create your views here.


class CreateTaskView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    def post(self, request):
        
        
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            assigned_to = serializer.validated_data['assigned_to']

            if assigned_to.company != request.user.company:
                return Response({
                    "error":"Cannot assign task outside your company"
                },
                status= status.HTTP_400_BAD_REQUEST
                )
            
            task = serializer.save(
                company = request.user.company,
                assigned_by = request.user
            )
            Notification.objects.create(
                recipient=assigned_to,
                title="New Task Assigned",
                message=
                f"You have been assigned "
                f"task '{task.title}'"
            )

# AUDIT LOG OBJECT CREATION
            AuditLog.objects.create(
                company = request.user.company,
                actor = request.user,
                action = "CREATE",
                entity_type = "TASK",
                entity_id=task.id,
                description=f"{request.user.username} created task '{task.title}'"
            )


            return Response({
                "message":"Task Created Successfully"
            },
            status = status.HTTP_201_CREATED
            )
        print(serializer.errors)
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )
    
class MyTasksView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        tasks = Tasks.objects.filter(
            assigned_to = request.user
        )

        serializer = TaskSerializer(tasks, many = True)

        return Response(serializer.data)
    
class UpdateTaskStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            task = Tasks.objects.get(pk=pk)
        except Tasks.DoesNotExist:
            return Response(
                {
                    "error":"Task Not Found"
                },
                status = status.HTTP_404_NOT_FOUND
            )
        if task.assigned_to != request.user:
            return Response({
                "error":"You can Update only your own tasks"
            },
            status = status.HTTP_403_FORBIDDEN)
        
        serializer = UpdateTaskStatusSerializer(
            task,
            data = request.data,
            partial=True
        )
        if serializer.is_valid():
            old_status = task.status
            serializer.save()
            new_status = task.status
            
# AUDIT LOG OBJECT CREATION
            AuditLog.objects.create(
                company = request.user.company,
                actor = request.user,
                action = "UPDATE",
                entity_type = "TASK",
                entity_id=task.id,
                description=f"{request.user.username} changed task '{task.title}' status from {old_status} to {new_status}"
            )

            return Response({
                "message":"Task Status Updated Successfully"
            },
            status = status.HTTP_200_OK
            )
        
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class ViewCompanyTasks(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    def get(self,request):
        
        tasks = Tasks.objects.filter(company=request.user.company)
        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data)