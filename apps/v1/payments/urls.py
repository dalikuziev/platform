from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, PaymentStudentsListView

router = DefaultRouter()
router.register('', PaymentViewSet, basename='payments')

urlpatterns = [
    path('my-payments/', PaymentStudentsListView.as_view(), name='my-payments'),
    path('', include(router.urls)),
]