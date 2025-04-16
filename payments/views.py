from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

# class PaymentFilter(django_filters.FilterSet):
#     category = django_filters.CharFilter(field_name='category', lookup_expr='iexact')
#     is_draft = django_filters.BooleanFilter()

    # class Meta:
    #     model = Payment

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-paid_at')
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filterset_class = PaymentFilter



