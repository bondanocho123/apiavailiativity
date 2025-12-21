from django.db import models
from django.conf import settings

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")

    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username