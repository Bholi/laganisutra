from rest_framework import serializers
from .models import RsiSummary,MacdSummary,AdxSummary,CciSummary,StochRsiSummary,AoSummary,UoSummary,VwmaSummary,BopSummary,WillRSummary,MomentumSummary

class RsiSummaryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RsiSummary
        fields = '__all__'

class MacdSummaryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MacdSummary
        fields = '__all__'

class AdxSummaryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdxSummary
        fields = '__all__'

class CciSummaryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CciSummary
        fields = '__all__'

class StochRsiSummaryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StochRsiSummary
        fields = '__all__'


class MomentumSummaryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MomentumSummary
        fields = '__all__'

class AoSummaryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AoSummary
        fields = '__all__'

class UoSummaryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UoSummary
        fields = '__all__'

class VwmaSummaryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VwmaSummary
        fields = '__all__'


class WillRSummaryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WillRSummary
        fields = '__all__'


class BopSummaryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BopSummary
        fields = '__all__'