from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import InStockFilterBackend, OrderFilter
from .models import Order, OrderItem, Product
from .serializers import (OrderItemSerializer, OrderSerializer,
                          ProductInfoSerializer, ProductSerializer)

# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return JsonResponse({
#         'data': serializer.data
#     })

# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

# class ProductList(APIView):
#     def get(self, request):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return JsonResponse({'data': serializer.data})

# class ProductListAPIView(generics.ListAPIView):
#     # queryset = Product.objects.all()
#     def get_queryset(self):
#         # retrieve only the products whose stock is greater than 0.
#         products = Product.objects.all()
#         return [product for product in products if product.stock>0]
#     # OR Do:
#     # queryset = Product.objects.filter(stock__gt=0)
#     serializer_class = ProductSerializer


# @api_view(['GET'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product,id=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)  

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

# class ProductDetail(generics.RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer 

# class ProductDetail(APIView):
#     def get(self, request, pk):
#         product = Product.objects.get(id=pk)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)

# @api_view(['GET'])
# def order_list(request):
#     orders = Order.objects.prefetch_related(items__product)
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product').order_by('pk')
    serializer_class = OrderSerializer
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]

    @action(detail=False,
            methods=['GET'],
            url_path='user-orders',
            # permission_classes = [IsAuthenticated] # This is not necessary if you put the IsAuthenticated class into the permission_classes field of the OrderViewSet class.
        )
    def user_orders(self, request):
        orders = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    # @action(detail=False, methods=['POST'], url_path='create-orders')
    def list(self, request):
        orders = self.get_queryset()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

# class OrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product').order_by('pk')
#     serializer_class = OrderSerializer

# class UserOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product').order_by('pk')
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(user=self.request.user)

class ProductInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price'],
        })
        return Response(serializer.data)
    
# @api_view(['GET'])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer({
#         'products': products,
#         'count': len(products),
#         'max_price': products.aggregate(max_price=Max('price'))['max_price'],
#     })
#     return Response(serializer.data)

class ProductListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.order_by('pk')
    # filterset_fields = ['name', 'price']
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend,
    ]
    filterset_fields = {
        'name': ['iexact', 'icontains'],
        'price': ['lt', 'gt', 'range'],
    }

    search_fields = ['=name', 'description'] # This =name finds the exact match of the searched string in the name field of the existing products, and description still has icontains search property
    ordering_fields = ['name', 'price', 'stock']
    pagination_class = LimitOffsetPagination
    # pagination_class = PageNumberPagination
    # pagination_class.page_size = 4
    # pagination_class.max_page_size = 7
    # pagination_class.page_query_param = 'pagenum'
    # pagination_class.page_size_query_param = 'size'


    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     print(request.data)
    #     return super().create(request, *args, **kwargs)

# class CreateProductAPIView(generics.CreateAPIView):
#     serializer_class = ProductSerializer
#     model = Product

#     def create(self, request, *args, **kwargs): # This function in the current context is not necessary unless you want to customize the creation behavior.
#         print(request.data)
#         return super().create(request, *args, **kwargs)