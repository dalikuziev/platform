from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from config.config import ADMIN_URL, API_V1_URL, SWAGGER_URL
from config.settings import STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path(ADMIN_URL, admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
]

api_urls = [
    path(API_V1_URL+'auth/', include('apps.v1.accounts.urls')),
    path(API_V1_URL+'courses/', include('apps.v1.courses.urls')),
    path(API_V1_URL+'assignments/', include('apps.v1.assignments.urls')),
    path(API_V1_URL+'parents/', include('apps.v1.parents.urls')),
    path(API_V1_URL+'payments/', include('apps.v1.payments.urls')),
    path(API_V1_URL+'groups/', include('apps.v1.groups.urls')),
]

spectacular_urls = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path(SWAGGER_URL, SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

urlpatterns += api_urls
urlpatterns += spectacular_urls

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)