from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

# from .functions import generate_otp


User = get_user_model()


class UserProfile(models.Model):
    """
    Expands auth_user to include app specific information. Users are by default
    added to group 1. 
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar_id = models.IntegerField(blank=True, null=True)

    