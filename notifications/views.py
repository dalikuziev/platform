from rest_framework import viewsets
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

class NotificationFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category', lookup_expr='iexact')
    is_draft = django_filters.BooleanFilter()

    class Meta:
        model = Notification
        fields = ['category', 'is_draft']

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-scheduled_at')
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = NotificationFilter

