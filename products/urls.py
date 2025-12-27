from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CreateProductLinkView, UpdateProductLinkView, DeleteProductLinkView, ListProductLinksView, RetrieveProductLinkView
from .views import CreateProductImageView, ListProductImagesView, RetrieveProductImageView, UpdateProductImageView, DeleteProductImageView, SetPrimaryProductImageView, ReorderProductImagesView

urlpatterns = [
    path('create/', CreateProductLinkView.as_view(), name='create-product-link'),
    path('update/<int:id>/', UpdateProductLinkView.as_view(), name='update-product-link'),
    path('delete/<int:id>/', DeleteProductLinkView.as_view(), name='delete-product-link'),
    path('list/', ListProductLinksView.as_view(), name='list-product-links'),
    path('retrieve/<int:id>/', RetrieveProductLinkView.as_view(), name='retrieve-product-link'),

    path('product-images/', CreateProductImageView.as_view()),
    path('product-images/list/', ListProductImagesView.as_view()),
    path('product-images/<int:id>/', RetrieveProductImageView.as_view()),
    path('product-images/<int:id>/update/', UpdateProductImageView.as_view()),
    path('product-images/<int:id>/delete/', DeleteProductImageView.as_view()),
    path('product-images/<int:id>/set-primary/', SetPrimaryProductImageView.as_view()),
    path('product-images/reorder/', ReorderProductImagesView.as_view()),
]