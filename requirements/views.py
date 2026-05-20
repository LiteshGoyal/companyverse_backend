from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import RequirementSerializer, RequirementResponseSerializer, RequirementResponseViewSerializer, UpdateRequirementResponseStatusSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from auditlogs.models import AuditLog
from .models import Requirement, RequirementResponse
from companymultiverse.permissions import IsAdminOrManager
from companymultiverse.permissions import IsRequirementOwnerCompany

from notifications.models import Notification

# Create your views here.


class CreateRequirementView(APIView):
    permission_classes = [IsAuthenticated,
    IsAdminOrManager]
    def post(self, request):
        
        serializer = RequirementSerializer(data = request.data)
        if serializer.is_valid():
            requirement = serializer.save(company=request.user.company, created_by = request.user)

            AuditLog.objects.create(
                company = request.user.company,
                actor = request.user,
                action = "CREATE",
                entity_type = "Requirement",
                entity_id=requirement.id,
                description=f"{request.user.username} created requirement '{requirement.title}'"
            )

            return Response({
                "message":"Requirement Created Successfully"
            },
            status = status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    


class MarketplaceRequirementsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    def get(self, request):
        requirements = Requirement.objects.exclude(
            company = request.user.company
        ).filter(
            status="OPEN"
        )

        serializer = RequirementSerializer(
            requirements,
            many=True
        )

        return Response(serializer.data)
    
    
class MyRequirementsView(APIView):
    permission_classes=[IsAuthenticated, IsAdminOrManager]   

    def get(self, request):
        requirements = Requirement.objects.filter(
            company = request.user.company
        )
        
        serializer = RequirementSerializer(requirements,many=True)
        
        return Response(serializer.data)
    
    
    
class RespondToRequirementView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    def post(self, request, pk):
        
        try:
            requirement = Requirement.objects.get(pk=pk)

        except Requirement.DoesNotExist:
            return Response(
                {
                    "error": "Requirement not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if requirement.status == "CLOSED":
            return Response(
                {
                    "error": "Cannot respond to closed requirements"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if requirement.company == request.user.company:
            return Response({
                "error":"You cant respond to your own requirement"
            },
            status= status.HTTP_400_BAD_REQUEST
            )
            
        employee_id = request.data.get("employee")
        existing_response = RequirementResponse.objects.filter(requirement=requirement, company=request.user.company, employee_id=employee_id)
        
        if (existing_response):
            return Response({
                "error" : "You already proposed this employee"
            },
                status = status.HTTP_400_BAD_REQUEST
                            )
        
        serializer = RequirementResponseSerializer(data=request.data)

        if serializer.is_valid():
            employee = serializer.validated_data["employee"]
            if employee.company != request.user.company:
                return Response({
                    "error":"Employee must belong to your company"
                },
                status = status.HTTP_400_BAD_REQUEST
                )
            
            response=serializer.save(
                requirement=requirement,
                company = request.user.company,
                created_by= request.user
            )
            
            AuditLog.objects.create(
                company=request.user.company,
                actor=request.user,
                action="CREATE",
                entity_type="RequirementResponse",
                entity_id=response.id,
                description=f"{request.user.username} responded to requirement '{requirement.title}' with employee '{employee.username}'"
            )

            return Response(
                {
                    "message": "Response submitted successfully"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ViewRequirementResponsesView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrManager,
    IsRequirementOwnerCompany]

    def get(self, request, pk):
        
        try:
            requirement = Requirement.objects.get(pk=pk)

        except Requirement.DoesNotExist:
            return Response(
                {
                    "error": "Requirement not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(
            request,
            requirement
        )
        
        
        responses = RequirementResponse.objects.filter(
            requirement = requirement
        )

        serializer = RequirementResponseViewSerializer(responses, many=True)

        return Response(serializer.data)
    


class UpdateRequirementResponseStatusView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrManager,
    IsRequirementOwnerCompany]

    def patch(self, request, pk):
        
        try:
            response = RequirementResponse.objects.get(pk=pk)

        except RequirementResponse.DoesNotExist:
            return Response(
                {
                    "error": "Response not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        self.check_object_permissions(
            request,
            response
        )
        

        serializer = UpdateRequirementResponseStatusSerializer(
            response,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            old_status = response.status

            serializer.save()
            if serializer.instance.status == "ACCEPTED":

                requirement = serializer.instance.requirement

                requirement.status = "CLOSED"

                requirement.save()

            AuditLog.objects.create(
                company=request.user.company,
                actor=request.user,
                action="UPDATE",
                entity_type="RequirementResponse",
                entity_id=str(response.id),
                description=f"{request.user.username} changed response status from {old_status} to {response.status}"
            )
            if response.status == "ACCEPTED":

                Notification.objects.create(

                    recipient=response.employee,

                    title="Requirement Accepted",

                    message=
                    "Your requirement response "
                    "was accepted"
                )

            return Response(
                {
                    "message": "Response status updated successfully"
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class CloseRequirementView(APIView):

    permission_classes = [IsAuthenticated, IsAdminOrManager,
    IsRequirementOwnerCompany]

    def patch(self, request, pk):

        try:
            requirement = Requirement.objects.get(pk=pk)

        except Requirement.DoesNotExist:
            return Response(
                {
                    "error": "Requirement not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(
            request,
            requirement
        )


        requirement.status = "CLOSED"
        requirement.save()

        AuditLog.objects.create(
            company=request.user.company,
            actor=request.user,
            action="UPDATE",
            entity_type="Requirement",
            entity_id=str(requirement.id),
            description=f"{request.user.username} closed requirement '{requirement.title}'"
        )

        return Response(
            {
                "message": "Requirement closed successfully"
            },
            status=status.HTTP_200_OK
        )