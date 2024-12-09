
from .models import Ema5Model,Ema100Model,Ema20Model,Ema30Model,Ema50Model,Ema10Model,Ema200Model
from .serializers import Ema5ModelSerializer,Ema100ModelSerializer,Ema10ModelSerializer,Ema20ModelSerializer,Ema30ModelSerializer,Ema50ModelSerializer,Ema200ModelSerializer
import pandas as pd
from rest_framework import status
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils.dateparse import parse_date
from django.db.models import Max
# Create your views here.




@api_view(['GET'])
def ema5_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = Ema5Model.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = Ema5ModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def ema10_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = Ema10Model.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = Ema10ModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def ema20_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = Ema20Model.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = Ema20ModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def ema30_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = Ema30Model.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = Ema30ModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def ema50_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = Ema50Model.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = Ema50ModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def ema100_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = Ema100Model.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = Ema100ModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def ema200_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = Ema200Model.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = Ema200ModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)