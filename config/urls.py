from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

admin.autodiscover()

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
    path('email/', include('emailbackend.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]

if 'silk' in settings.INSTALLED_APPS:
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
