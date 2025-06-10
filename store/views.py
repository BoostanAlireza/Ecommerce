from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .filters import ProductFilter
from .models import Cart, CartItem, Category, Customer, Order, OrderItem, Product, Comment, ProductImage
from .signals import order_created
from .pagination import CustomPageNumberPagination
from .permissions import IsAdminOrReadOnly
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CommentSerializer, CustomerSerializer, OrderCreateSerializer, OrderForAdminSerializer, OrderSerializer, OrderUpdateSerializer, ProductImageSerializer, ProductSerializer, CategorySerializer, UpdateCartItemSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, pk):
        product = get_object_or_404(
            Product.objects.select_related('category'), pk=pk
        )
        if product.order_items.count() > 0:
            return Response({'error': 'There are some order items including this one. Please remove them first.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_serializer_context(self):
        return {'product_pk': self.kwargs['product_pk']}

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        product_pk = self.kwargs['product_pk']
        return Comment.approved.filter(product_id=product_pk).all()

    def get_serializer_context(self):
        return {'product_pk': self.kwargs['product_pk']}


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user_id = request.user.id
        customer = Customer.objects.get(user_id=user_id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        cart_pk = self.kwargs['cart_pk']
        return CartItem.objects.select_related('product').filter(cart_id=cart_pk).all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_pk': self.kwargs['cart_pk']}


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):

    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'options', 'head']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = Order.objects.prefetch_related(
            Prefetch(
                'items',
                queryset=OrderItem.objects.select_related('product')
            )
        ).select_related('customer__user').all()

        user = self.request.user

        if user.is_staff:
            return queryset

        return queryset.filter(customer__user_id=user.id)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer

        if self.request.method == 'PATCH':
            return OrderUpdateSerializer

        if self.request.user.is_staff:
            return OrderForAdminSerializer
        return OrderSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def create(self, request, *args, **kwargs):
        create_order_serializer = OrderCreateSerializer(
            data=request.data,
            context={'user_id': self.request.user.id}
        )
        create_order_serializer.is_valid(raise_exception=True)
        created_order = create_order_serializer.save()

        order_created.send_robust(self.__class__, order=created_order)

        serializer = OrderSerializer(created_order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
