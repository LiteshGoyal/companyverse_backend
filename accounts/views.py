from django.shortcuts import render
from .serializers import RegisterSerializer, UserSerializer, UpdateProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from auditlogs.models import AuditLog
# Create your views here.

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User registered successfully"
            },
            status = status.HTTP_201_CREATED
        )
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )
    
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)

        return Response(serializer.data)
    

class UpdateProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request):

        serializer = UpdateProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            AuditLog.objects.create(
                company=request.user.company,
                actor=request.user,
                action="UPDATE",
                entity_type="User",
                entity_id=str(request.user.id),
                description=f"{request.user.username} updated profile"
            )

            return Response(
                {
                    "message": "Profile updated successfully"
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )