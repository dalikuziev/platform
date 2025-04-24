from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from config.config import ADMIN_URL
from config.settings import STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path(ADMIN_URL, admin.site.urls),
    path('api/auth/', include('apps.v1.accounts.urls')),
    path('api/courses/', include('apps.v1.courses.urls')),
    path('api/assignments/', include('apps.v1.assignments.urls')),
    path('api/parents/', include('apps.v1.parents.urls')),
    path('api/payments/', include('apps.v1.payments.urls')),
    path('api/groups/', include('apps.v1.groups.urls')),
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