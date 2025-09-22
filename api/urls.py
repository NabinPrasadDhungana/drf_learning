from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListAPIView.as_view()),
    path('product/<int:pk>/', views.ProductDetailAPIView.as_view()),
    path('product/info/', views.product_info),
    path('orders/', views.order_list)
]
