from rest_framework import serializers
from .models import Tasks
from accounts.models import User

class TaskSerializer(serializers.ModelSerializer):
    # Stringrelatedfieldd returns email instead of just id
    assigned_by = serializers.StringRelatedField()
    assigned_to = serializers.PrimaryKeyRelatedField(
            queryset=User.objects.all(),
            write_only=True
        )

    assigned_to_name = serializers.StringRelatedField(
            source="assigned_to",
            read_only=True
        )

    class Meta:
        model = Tasks

        fields = [
            "id",
            "title",
            "description",
            "assigned_to",
            "assigned_to_name",
            "assigned_by",
            "status",
            "deadline",
            "created_at",
        ]

class UpdateTaskStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tasks

        fields = [
            "status"
        ]