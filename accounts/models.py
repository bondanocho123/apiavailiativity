from django.db import models
from django.conf import settings
from campaigns.models import Racks
from products.models import ProductLinks

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")

    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        app_label = 'accounts'
        
    def __str__(self):
        return self.user.username
class AffiliateAccounts (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="affiliate_accounts")

    affiliate_name = models.CharField(max_length=100)
    affiliate_link = models.CharField(max_length=100) #generate url availiativity
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.platform} - {self.affiliate_id}"

