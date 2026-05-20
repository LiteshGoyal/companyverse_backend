from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import EmployeeRatingSerializer
from auditlogs.models import AuditLog
from companymultiverse.permissions import IsAdminOrManager
from .models import EmployeeRating
from accounts.models import User

from notifications.models import Notification


class RateEmployeeView(APIView):

    permission_classes = [IsAuthenticated,
    IsAdminOrManager]

    def post(self, request):

        

        serializer = EmployeeRatingSerializer(
            data=request.data
        )

        if serializer.is_valid():

            employee = serializer.validated_data["employee"]

            if employee.company != request.user.company:
                return Response(
                    {
                        "error": "Employee must belong to your company"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if employee == request.user:
                return Response(
                    {
                        "error": "You cannot rate yourself"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            rating = serializer.save(
                company=request.user.company,
                rated_by=request.user
            )
            Notification.objects.create(

                recipient=employee,

                title="New Performance Rating",

                message=
                f"You received a "
                f"{rating.rating}/5 rating"
            )

            AuditLog.objects.create(
                company=request.user.company,
                actor=request.user,
                action="CREATE",
                entity_type="EmployeeRating",
                entity_id=str(rating.id),
                description=f"{request.user.username} rated {employee.username} with {rating.rating}"
            )

            return Response(
                {
                    "message": "Employee rated successfully"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
        
        

class EmployeeRatingsView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, employee_id):

        try:

            employee = User.objects.get(
                pk=employee_id
            )

        except User.DoesNotExist:

            return Response(
                {
                    "error":
                    "Employee not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if (
            employee.company !=
            request.user.company
        ):

            return Response(
                {
                    "error":
                    "You cannot view ratings outside your company"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        ratings = EmployeeRating.objects.filter(
            employee=employee
        ).order_by("-created_at")

        serializer = EmployeeRatingSerializer(
                ratings,
                many=True
            )

        return Response(serializer.data)