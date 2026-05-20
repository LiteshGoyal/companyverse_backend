from rest_framework.views import APIView
from companymultiverse.permissions import (
    IsEmployee
)
from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.response import (
    Response
)

from companymultiverse.permissions import (
    IsAdminOrManager
)

from accounts.models import User

from tasks.models import Tasks

from requirements.models import Requirement

from notifications.models import (
    Notification
)

from ratings.models import EmployeeRating


class DashboardStatsView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        company = request.user.company

        if request.user.role in [
            "ADMIN",
            "MANAGER"
        ]:

            employees = User.objects.filter(
                    company=company
                ).count()

            pending_tasks = Tasks.objects.filter(
                    company=company,
                    status="TODO"
                ).count()

            completed_tasks = Tasks.objects.filter(
                    company=company,
                    status="COMPLETED"
                ).count()

            requirements = Requirement.objects.filter(
                    company=company
                ).count()

            unread_notifications = Notification.objects.filter(
                    recipient=request.user,
                    is_read=False
                ).count()

            ratings = EmployeeRating.objects.filter(
                    company=company
                )

            average_rating = None

            if ratings.exists():

                total = 0

                for rating in ratings:

                    total += float(
                        rating.rating
                    )

                average_rating = round(
                    total / ratings.count(),
                    1
                )

            return Response({

                "dashboard_type":
                    "ADMIN",

                "employees":
                    employees,

                "pending_tasks":
                    pending_tasks,

                "completed_tasks":
                    completed_tasks,

                "requirements":
                    requirements,

                "unread_notifications":
                    unread_notifications,

                "average_rating":
                    average_rating,
            })

        employee_tasks = Tasks.objects.filter(
                assigned_to=request.user
            )
        
        unread_notifications = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()

        return Response({

            "dashboard_type":
                "EMPLOYEE",

            "my_tasks":
                employee_tasks.count(),

            "completed_tasks":
                employee_tasks.filter(
                    status="COMPLETED"
                ).count(),

            "pending_tasks":
                employee_tasks.filter(
                    status="TODO"
                ).count(),

             "unread_notifications":
        unread_notifications,
        })