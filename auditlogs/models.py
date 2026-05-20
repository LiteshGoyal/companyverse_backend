from django.db import models
from django.conf import settings
# Create your models here.
class AuditLog(models.Model):

    ACTION_CHOICES = (
        ("CREATE","Create"),
        ("UPDATE","Update"),
        ("DELETE","Delete"),
        ("ASSIGN","Assign"),
        ("TRANSFER","Transfer"),
    )

    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE, related_name="audit_logs")
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="performed_audit_logs"
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    entity_type = models.CharField(max_length=100)
    entity_id = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor} - {self.action}"
    
