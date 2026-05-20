from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Notification
from .serializers import NotificationSerializer

class MyNotificationsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        notifications = Notification.objects.filter(
            recipient = request.user
        )

        serializer = NotificationSerializer(notifications, many=True)
        
        return Response(serializer.data)

class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]  
    def patch(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, recipient = request.user)
        except Notification.DoesNotExist:
            return Response({
                "error":"Notification Not Found"
            },
                            status = status.HTTP_404_NOT_FOUND
                            )
        
        notification.is_read = True
        notification.save()
        
        return Response({
            "message":"Notification marked as read"
        },
                        status =status.HTTP_200_OK
                        )