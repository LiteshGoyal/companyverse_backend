from rest_framework import serializers
from .models import Company
from accounts.models import User

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields=[
            'id','name','description'
        ]



class EmployeeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "email",
            "role",
            "skills",
            "experience_years",
            "current_position",
        ]
        
        
class EmployeeDetailSerializer(
    serializers.ModelSerializer
):

    average_rating = serializers.SerializerMethodField()

    class Meta:

        model = User

        fields = [

            "id",

            "username",

            "email",

            "role",

            "skills",

            "experience_years",

            "current_position",

            "bio",

            "average_rating",
        ]

    def get_average_rating(
        self,
        obj
    ):

        ratings = obj.received_ratings.all()

        if not ratings.exists():

            return None

        total = 0

        for rating in ratings:

            total += float(
                rating.rating
            )

        return round(
            total / ratings.count(),
            1
        )