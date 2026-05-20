from .models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
        ]

        extra_kwargs = {
            'password' : {'write_only': True}

        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data["email"],
            username = validated_data['username'],
            password = validated_data['password']
        )

        return user
    
class UserSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
            "company"
        ]

class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            "skills",
            "experience_years",
            "bio",
            "current_position",
        ]