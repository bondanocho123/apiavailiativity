from django.db import models
from django.conf import settings
from products.models import ProductLinks
from racks.models import Racks

# Create your models here.

class CampaignTemplates(models.Model):
    """
    Template konten untuk kampanye di sosial media
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="campaign_templates")

    PLATFORM_CHOICES = [
        ('x', 'X / Twitter'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('threads', 'Threads'),
        ('tiktok', 'TikTok'),
        ('whatsapp', 'WhatsApp'),
    ]

    name = models.CharField(max_length=100)
    platform = models.CharField(choices=PLATFORM_CHOICES, max_length=50)
    content_template = models.TextField(
        help_text="Gunakan placeholder seperti {product_name}, {affiliate_link}, {rack_name}"
    )
    image_template_url = models.URLField(blank=True, null=True)
    
    # Opsional: template bisa terkait dengan rack atau produk tertentu
    related_rack = models.ForeignKey(Racks, on_delete=models.SET_NULL, null=True, blank=True)
    related_product = models.ForeignKey(ProductLinks, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'campaigns'
        
    def __str__(self):
        return f"{self.name} ({self.get_platform_display()})"