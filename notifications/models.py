from django.db import models
import uuid

from django.db import models

from accounts.models import User

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable=False)
    
    recipient = models.ForeignKey(User, on_delete = models.CASCADE, related_name="notifications")
    
    title = models.CharField(
        max_length=255
    )
    
    message = models.TextField()
    is_read = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    class Meta:
        ordering = ["-created_at"]
        
    def __str__(self):
        return (f"{self.recipient.username} - "
    f"{self.title}")