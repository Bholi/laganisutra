from rest_framework import serializers
from .models import SupportResistance

class SrSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportResistance
        fields = '__all__'