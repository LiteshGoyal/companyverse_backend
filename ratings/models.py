from django.db import models
from django.conf import settings


class EmployeeRating(models.Model):

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="employee_ratings"
    )

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_ratings"
    )

    rated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="given_ratings"
    )

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1
    )

    feedback = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.employee} - {self.rating}"