from .models import SubIndices
from rest_framework import serializers

class SubIndicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubIndices
        fields = '__all__'