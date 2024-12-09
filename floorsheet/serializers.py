from rest_framework import serializers
from .models import FloorSheetData,StockSummaryReport,BuyerActivityReport,SellerActivityReport,HighValueTransactionReport,VolatilityAnalysisReport,TradeVolAnalysisReport,PriceMovementAnalysisReport,LiquidityConcentrationReport,PriceVolatilityVolumeReport,PriceElasticityDemandReport,StockPriceRangeReport,BrokerVolumeConcentrationReport,Sector

class FloorSheetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorSheetData
        fields = '__all__'  # Include all fields


class StockSummaryReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockSummaryReport
        fields = '__all__'

class BuyerActivityReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerActivityReport
        fields = '__all__'

class SellerActivityReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerActivityReport
        fields = '__all__'


class HighValueReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = HighValueTransactionReport
        fields='__all__'

class VolatilityAnalysisReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolatilityAnalysisReport
        fields='__all__'

class TradeVolumeAnalysisReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeVolAnalysisReport
        fields='__all__'

class PriceMovementAnalysisReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceMovementAnalysisReport
        fields='__all__'

class LCRReportSerializer(serializers.ModelSerializer):
    class Meta:
        model= LiquidityConcentrationReport
        fields= '__all__'

class PVVRSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceVolatilityVolumeReport
        fields = '__all__'

class PriceElasticitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceElasticityDemandReport
        fields = '__all__'

class StockPriceRangeReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPriceRangeReport
        fields = '__all__'


class BrokerVolumeConcReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrokerVolumeConcentrationReport
        fields = '__all__'


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'