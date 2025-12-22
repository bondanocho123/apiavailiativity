from django.shortcuts import render
from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, permissions, status
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ProductLinkSerializer
from .models import ProductLinks
from .responses import BaseResponseMixin

# Create your views here.
class CreateProductLinkView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductLinkSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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