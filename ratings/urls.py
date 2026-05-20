from django.urls import path
from .views import RateEmployeeView, EmployeeRatingsView

urlpatterns = [
    path(
        "rate/",
        RateEmployeeView.as_view(),
        name="rate_employee_view"
    ),
    path(
        "employee/<uuid:employee_id>/",
        EmployeeRatingsView.as_view(),
        name="employee_ratings_view"
    ),
]