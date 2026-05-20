from django.db import models
from django.conf import settings

# Create your models here.
class Requirement(models.Model):

    STATUS_CHOICES = (
        ("OPEN","Open"),
        ("CLOSED","Closed"),
    )

    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE,related_name="requirements")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    required_skills = models.CharField(max_length=255)
    experience_required = models.IntegerField()
    offered_salary = models.IntegerField()
    offered_compensation = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="OPEN"
    )
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title
    

class RequirementResponse(models.Model):
    STATUS_CHOICES = (
    ("PENDING", "Pending"),
    ("ACCEPTED", "Accepted"),
    ("REJECTED", "Rejected"),
)
    requirement = models.ForeignKey("requirements.Requirement", on_delete=models.CASCADE, related_name="responses")
    company = models.ForeignKey("companies.Company", on_delete = models.CASCADE)
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="requirement_responses")
    message = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices= STATUS_CHOICES,
        default="PENDING"
    )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="created_requirement_responses")
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company} -> {self.requirement.title}"