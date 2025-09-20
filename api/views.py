from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .serializers import ProductSerializer, OrderItemSerializer, OrderSerializer
from .models import Product, Order, OrderItem
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return JsonResponse({
#         'data': serializer.data
#     })

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# class ProductList(APIView):
#     def get(self, request):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return JsonResponse({'data': serializer.data})

# class ProductList(ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product,id=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)  

# class ProductDetail(RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer 

# class ProductDetail(APIView):
#     def get(self, request, pk):
#         product = Product.objects.get(id=pk)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)

@api_view(['GET'])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
