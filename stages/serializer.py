from rest_framework import serializers
from .models import MarketCycleStage

class StagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketCycleStage
        fields = '__all__'