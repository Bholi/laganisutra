from .models import Sma5Model,Sma10Model,Sma20Model,Sma30Model,Sma50Model,Sma100Model,Sma200Model
from rest_framework import serializers

class Sma5ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sma5Model
        fields = '__all__'

class Sma10ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sma10Model
        fields = '__all__'

class Sma20ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sma20Model
        fields = '__all__'

class Sma30ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sma30Model
        fields = '__all__'

class Sma50ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sma50Model
        fields = '__all__'

class Sma100ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sma100Model
        fields = '__all__'

class Sma200ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sma200Model
        fields = '__all__'