from .models import Sma5Model,Sma10Model,Sma20Model,Sma30Model,Sma50Model,Sma100Model,Sma200Model
from .serializers import Sma5ModelSerializer,Sma10ModelSerializer,Sma20ModelSerializer,Sma30ModelSerializer,Sma50ModelSerializer,Sma100ModelSerializer,Sma200ModelSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse
import pandas as pd
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from django.db.models import Max
# Create your views here.


@api_view(['GET'])
def sma5_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = Sma5Model.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = Sma5ModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def sma10_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = Sma10Model.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = Sma10ModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def sma20_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = Sma20Model.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = Sma20ModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def sma30_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = Sma30Model.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = Sma30ModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def sma50_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = Sma50Model.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = Sma50ModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def sma100_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = Sma100Model.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = Sma100ModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def sma200_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = Sma200Model.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = Sma200ModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)