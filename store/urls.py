from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

app_name = 'store'
router = DefaultRouter()

router.register('products', views.ProductViewSet, basename='product')
router.register('categories', views.CategoryViewSet, basename='category')
router.register('customers', views.CustomerViewSet, basename='customer')
router.register('carts', views.CartViewSet, basename='cart')
router.register('orders', views.OrderViewSet, basename='order')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('comments', views.CommentViewSet, basename='product-comments')
products_router.register('images', views.ProductImageViewSet, basename='product-images')

cart_items_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_items_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + cart_items_router.urls + products_router.urls