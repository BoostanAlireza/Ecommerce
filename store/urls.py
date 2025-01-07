from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('products', views.ProductViewSet, basename='product')
router.register('categories', views.CategoryViewSet, basename='category')
router.register('customers', views.CustomerViewSet, basename='customer')

urlpatterns = router.urls
