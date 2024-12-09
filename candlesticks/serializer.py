from rest_framework import serializers
from .models import CandlestickPattern

class CandlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandlestickPattern
        fields = '__all__'