from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Company
from accounts.models import User

#pre_delete is a Django signal that fires just before a database object is deleted.
@receiver(pre_delete, sender=Company)
def reset_company_users(sender, instance, **kwargs):
    # Updates all matching users in a single, fast SQL command
    User.objects.filter(company=instance).update(
        company=None, 
        role=""
    )