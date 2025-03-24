"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


admin.site.site_header = 'Store'
admin.site.index_title = 'Special Access'


urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('store/', include('store.urls')),
    path('store/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('store/schema/docs', SpectacularSwaggerView.as_view(url_name='schema')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('payment/', include('payment.urls')),
    path('email/', include('emailbackend.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]

if 'silk' in settings.INSTALLED_APPS:
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
