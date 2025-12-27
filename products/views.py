from django.shortcuts import render
from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, permissions, status
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ProductLinkSerializer, ProductImageSerializer
from .models import ProductLinks, ProductImages
from .responses import BaseResponseMixin
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.
class CreateProductLinkView(BaseResponseMixin, generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductLinkSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return self.success_response(
                data=serializer.data,
                message="Produk berhasil ditambahkan",
                code=status.HTTP_201_CREATED
            )    
        except ValidationError as e :
            return self.error_response(
                message="Validasi gagal",
                errors=e.detail,
                code=status.HTTP_400_BAD_REQUEST
            )

        
    

class UpdateProductLinkView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductLinkSerializer
    queryset = ProductLinks.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        return ProductLinks.objects.filter(user=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save()

class DeleteProductLinkView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ProductLinks.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        return ProductLinks.objects.filter(user=self.request.user)
    
    def perform_destroy(self, instance):
        instance.delete()

class ListProductLinksView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductLinkSerializer

    def get_queryset(self):
        return ProductLinks.objects.filter(user=self.request.user)
    
class RetrieveProductLinkView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductLinkSerializer
    queryset = ProductLinks.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        return ProductLinks.objects.filter(user=self.request.user)
    

class CreateProductImageView(BaseResponseMixin, generics.CreateAPIView): 
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductImageSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer) :
        product_id = self.request.data.get("product_link")

        product = ProductLinks.objects.filter(
            id=product_id,
            user = self.request.user
        ).first()

        if  not product :
            raise ValidationError({ "product_link" : "Produk tidak ditemukan"})
        
        last_order = ProductImages.objects.filter(
            product_link=product
        ).count()

        serializer.save(
            product_link=product,
            order=last_order
        )

    def create(self, request, *args, **kwargs) :
        serializer = self.get_serializer(data=request.data)

        try :
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return self.success_response(
                data=serializer.data,
                message="Gambar produk berhasil ditambahkan",
                code=status.HTTP_201_CREATED
            )
        except ValidationError as e :
            return self.success_response(
                message="Validasi gagal",
                errors = e.detail,
                code=status.HTTP_400_BAD_REQUEST
            )

class ListProductImagesView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        product_id = self.request.query_params.get("product_id")

        return ProductImages.objects.filter(
            product_link__id = product_id,
            product_link__user = self.request.user
        ).order_by("order")
    
class RetrieveProductImageView(generics.RetrieveAPIView) :
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductImageSerializer
    lookup_field = "id"

    def get_queryset(self):
        return ProductImages.objects.filter(
            product_link__user=self.request.user
        )

class UpdateProductImageView(BaseResponseMixin, generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductImageSerializer
    lookup_field = "id"

    def get_queryset(self):
        return ProductImages.objects.filter(
            produk_link__user = self.request.user
        )
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Jika set primary
        if request.data.get("is_primary") is True:
            ProductImages.objects.filter(
                product_link=instance.product_link,
                is_primary=True
            ).exclude(id=instance.id).update(is_primary=False)

        return super().update(request, *args, **kwargs)
    
class DeleteProductImageView(BaseResponseMixin, generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return ProductImages.objects.filter(
            product_link__user=self.request.user
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return self.success_response(
            message="Gambar produk berhasil dihapus",
            code=status.HTTP_200_OK
        )
    
class SetPrimaryProductImageView(BaseResponseMixin, generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductImageSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return ProductImages.objects.filter(
            product_link__user=self.request.user
        )

    def patch(self, request, *args, **kwargs):
        image = self.get_object()

        ProductImages.objects.filter(
            product_link=image.product_link,
            is_primary=True
        ).exclude(id=image.id).update(is_primary=False)

        image.is_primary = True
        image.save(update_fields=['is_primary'])

        return self.success_response(
            message="Gambar utama berhasil diubah",
            code=status.HTTP_200_OK
        )

class ReorderProductImagesView(BaseResponseMixin, generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        """
        Payload:
        {
          "orders": [
            {"id": 1, "order": 0},
            {"id": 2, "order": 1},
            {"id": 3, "order": 2}
          ]
        }
        """
        orders = request.data.get("orders")

        if not isinstance(orders, list):
            return self.error_response(
                message="Payload tidak valid",
                code=status.HTTP_400_BAD_REQUEST
            )

        images = ProductImages.objects.filter(
            id__in=[o["id"] for o in orders],
            product_link__user=request.user
        )

        image_map = {img.id: img for img in images}

        for item in orders:
            img = image_map.get(item["id"])
            if img:
                img.order = item["order"]

        ProductImages.objects.bulk_update(image_map.values(), ['order'])

        return self.success_response(
            message="Urutan gambar berhasil diperbarui",
            code=status.HTTP_200_OK
        )