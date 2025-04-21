from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from config.settings import STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT
from config.config import ADMIN_URL, SWAGGER_URL
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path(ADMIN_URL, admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/assignments/', include('assignments.urls')),
    path('api/parents/', include('parents.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/groups/', include('groups.urls')),
]

# spectacular_urls = [
#     path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
#     # Optional UI:
#     path(SWAGGER_URL, SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
#     # path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
# ]
#
# urlpatterns += spectacular_urls
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
