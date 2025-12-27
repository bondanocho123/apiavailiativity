from django.db import models
from django.conf import settings
import uuid
import os

# Create your models here.
def product_image_path(instance, filename):
    """
    media/products/<user_id>/<product_id>/<uuid>.<ext>
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join(
        "products",
        str(instance.product_link.user.id),
        str(instance.product_link.id),
        filename
    )


class ProductLinks (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="product_links")

    PLATFORM_CHOICES = [
        ('tokopedia', 'Tokopedia'),
        ('shopee', 'Shopee'),
    ]
    source_marketplace = models.CharField(choices=PLATFORM_CHOICES, max_length=50)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True) #URL gambar utama produk
    image_urls = models.JSONField(blank=True, null=True) #Array URL gambar tambahan
    product_url = models.URLField() #URL produk original di marketplace
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'products'
        unique_together = ('user', 'product_url')  # Satu user tidak bisa add produk yang sama dua kali
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.source_marketplace} - {self.product_url}"
    
class ProductImages(models.Model):
    product_link = models.ForeignKey(ProductLinks, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(
        upload_to=product_image_path
    )
    is_primary = models.BooleanField(
        default=False,
        help_text="Menandai gambar utama produk"
    )
    
    order = models.PositiveIntegerField(
        default=0,
        help_text="Urutan tampilan gambar"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "products"
        ordering = ["order", "created_at"]
        indexes = [
            models.Index(fields=['product_link'])
        ]
    
    def __str__(self):
        return f"Image {self.id} - Product {self.product_link.id}"