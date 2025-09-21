from django.urls import path
from . import views

urlpatterns = [
    # path('products/', views.product_list),
    path('products/', views.ProductListAPIView.as_view()),
    path('product/<int:pk>/', views.product_detail),
    path('product/info/', views.product_info),
    # path('product/<int:pk>/', views.ProductDetail.as_view()),
    path('orders/', views.order_list)
]
