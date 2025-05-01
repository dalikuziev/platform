from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import PaymentSerializer
from ..accounts.permissions import IsAdmin, IsStudent


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-paid_at')
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    permission_classes = [IsAuthenticated, IsAdmin]
    http_method_names = ['post']

class PaymentStudentsListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsStudent]
    def get_queryset(self):
        return Payment.objects.filter(student=self.request.user)