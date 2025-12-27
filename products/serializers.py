from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import ProductLinks, ProductImages

class ProductLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLinks
        fields = ['id', 'product_url','image_url', 'image_urls', 'name', 'description', 'created_at', 'source_marketplace']

    def validate_product_url(self, value):
        user = self.context['request'].user
        qs = ProductLinks.objects.filter(user=user, product_url=value)

        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        
        if qs.exists():
            raise serializers.ValidationError("Produk dengan URL ini sudah ditambahkan.")
        
        return value
            
        
class ProductImageSerializer(serializers.ModelSerializer):

    class Meta :
        model = ProductImages
        fields = [
            "id",
            "image",
            "is_primary",
            "order",
            "created_at"
        ]

        read_only_fields = ["created_at"]

    def validate_image(self, value):
        if value.size > 5*1024 * 1024:
            raise serializers.ValidationError("Maksimal 5MB")
        
        return value
    
    def validate_order(self, value) :
        if value < 0 :
            raise serializers.ValidationError("Order tidak valid")
        
        return value