from .models import Ema5Model,Ema100Model,Ema20Model,Ema30Model,Ema50Model,Ema200Model,Ema10Model
from rest_framework import serializers

class Ema5ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ema5Model
        fields = '__all__'

class Ema10ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ema10Model
        fields = '__all__'

class Ema20ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ema20Model
        fields = '__all__'

class Ema30ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ema30Model
        fields = '__all__'

class Ema50ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ema50Model
        fields = '__all__'

class Ema100ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ema100Model
        fields = '__all__'

class Ema200ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ema200Model
        fields = '__all__'