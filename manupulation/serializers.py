from rest_framework import serializers
from .models import TradeAnalysis,BoilerRoom,EmbezzlementData,LayeringSpoofingData,PonziSchemeData,RampingData,ThresholdTuningData,WashTradeData

class TradeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeAnalysis
        fields = '__all__'


class BoilerRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoilerRoom
        fields = '__all__'

class EmbezzlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmbezzlementData
        fields = '__all__'

class LayeringSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayeringSpoofingData
        fields = '__all__'

class PonziSerializer(serializers.ModelSerializer):
    class Meta:
        model = PonziSchemeData
        fields = '__all__'

class RampingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RampingData
        fields = '__all__'

class ThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThresholdTuningData
        fields = '__all__'

class WashingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WashTradeData
        fields = '__all__'