from .models import PivotPoint,FibonacciPivotPoint,CamrillaPivotPoint
from rest_framework import serializers

class PivotPointModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PivotPoint
        fields = '__all__'


class FibonacciPivotPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = FibonacciPivotPoint
        fields = '__all__'

class CamarillaPivotPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = CamrillaPivotPoint
        fields = '__all__'

