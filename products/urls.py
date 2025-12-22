from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CreateProductLinkView, UpdateProductLinkView, DeleteProductLinkView, ListProductLinksView, RetrieveProductLinkView

urlpatterns = [
    path('create/', CreateProductLinkView.as_view(), name='create-product-link'),
    path('update/<int:id>/', UpdateProductLinkView.as_view(), name='update-product-link'),
    path('delete/<int:id>/', DeleteProductLinkView.as_view(), name='delete-product-link'),
    path('list/', ListProductLinksView.as_view(), name='list-product-links'),
    path('retrieve/<int:id>/', RetrieveProductLinkView.as_view(), name='retrieve-product-link'),
]