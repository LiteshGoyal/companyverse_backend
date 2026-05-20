from rest_framework import serializers
from .models import EmployeeRating


class EmployeeRatingSerializer(serializers.ModelSerializer):
    rated_by = serializers.StringRelatedField()
    class Meta:
        model = EmployeeRating

        fields = [
            "employee",
            "rating",
            "feedback",
            "rated_by",
            "created_at",
        ]