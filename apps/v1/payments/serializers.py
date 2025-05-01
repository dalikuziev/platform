from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        # extra_kwargs = {
        #     'graded_by': {'required': True},
        # }