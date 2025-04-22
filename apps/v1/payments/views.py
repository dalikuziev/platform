from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from .models import Payment
from .serializers import PaymentSerializer


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
