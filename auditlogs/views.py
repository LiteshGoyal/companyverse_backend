from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework.response import Response
from companymultiverse.permissions import (
    IsAdminOrManager
)
from .models import AuditLog
from .serializers import (
    AuditLogSerializer
)

class CompanyAuditLogsView(
    APIView
):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrManager
    ]

    def get(self, request):

        logs =  AuditLog.objects.filter(
                company=request.user.company
            ).order_by("-created_at")

        serializer = AuditLogSerializer(
                logs,
                many=True
            )

        return Response(
            serializer.data
        )