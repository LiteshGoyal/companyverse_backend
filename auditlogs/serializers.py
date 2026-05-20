from rest_framework import serializers

from .models import AuditLog


class AuditLogSerializer(
    serializers.ModelSerializer
):
    actor = serializers.StringRelatedField()
    class Meta:
        model = AuditLog
        fields = [
            "id",
            "actor",
            "action",
            "entity_type",
            "entity_id",
            "description",
            "created_at",
        ]