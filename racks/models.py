from django.db import models
from django.conf import settings
from products.models import ProductLinks

# Create your models here.
class Racks (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="racks")

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'racks'

    def __str__(self):
        return self.name

class RackItems (models.Model):
    rack = models.ForeignKey(Racks, on_delete=models.CASCADE, related_name="items")
    product_link = models.ForeignKey(ProductLinks, on_delete=models.CASCADE, related_name="rack_items")

    position = models.PositiveIntegerField(default=0)
    item_name = models.CharField(max_length=100)
    item_description = models.TextField(blank=True, null=True)
    item_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'racks'
        unique_together = ('rack', 'product_link')  # Satu produk hanya sekali per rack
        ordering = ['position', 'created_at']
    def __str__(self):
        return self.item_name