from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .filters import ProductFilter
from .models import Category, Customer, Product
from .pagination import CustomPageNumberPagination
from .serializers import CustomerSerializer, ProductSerializer, CategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    pagination_class = CustomPageNumberPagination

    def destroy(self, request, pk):
        product = get_object_or_404(
            Product.objects.select_related('category'), pk=pk
        )
        if product.order_items.count() > 0:
            return Response({'error': 'There are some order items including this one. Please remove them first.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer