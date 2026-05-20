from .models import Requirement, RequirementResponse
from rest_framework import serializers
from accounts.models import User


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields=[
            'id',
            'title',
            'description',
            'required_skills',
            'experience_required',
            'offered_salary',
            'offered_compensation',
            'status'
        ]

class RequirementResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequirementResponse
        fields=[
            'employee',
            'message',
        ]


class EmployeeProfileSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "email",
            "skills",
            "experience_years",
            "bio",
            "current_position",
            "average_rating",
        ]
    def get_average_rating(self, obj):

        ratings = obj.received_ratings.all()

        if not ratings.exists():
            return None

        total = 0

        for rating in ratings:
            total += float(rating.rating)

        return round(total / ratings.count(), 1)


class RequirementResponseViewSerializer(serializers.ModelSerializer):
    employee = EmployeeProfileSerializer()
    company = serializers.StringRelatedField()
    contact_email = serializers.SerializerMethodField()
    class Meta:
        model = RequirementResponse
        fields=[
            'id',
            'employee',
            'company',
            'message',
            'status',
            "contact_email",
            'created_at'
        ]
    def get_contact_email(self, obj):

        if obj.status == "ACCEPTED":
            return obj.company.owner.email

        return None

class UpdateRequirementResponseStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequirementResponse

        fields = [
            "status"
        ]