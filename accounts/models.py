from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees"
    )

    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("MANAGER", "Manager"),
        ("EMPLOYEE", "Employee"),
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        null=True,
        blank=True
    )

    skills = models.TextField(blank=True, null=True)

    experience_years = models.IntegerField(
        blank=True,
        null=True
    )

    bio = models.TextField(blank=True, null=True)

    current_position = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


    def __str__(self):
        return self.email