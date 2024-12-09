from .models import AllScriptsData
from rest_framework import serializers

class AllScriptsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllScriptsData
        fields = '__all__'