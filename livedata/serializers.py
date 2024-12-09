from rest_framework import serializers
from .models import LiveFeedData


class LiveDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveFeedData
        fields = '__all__'