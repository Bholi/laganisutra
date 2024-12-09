from .models import PivotPoint,FibonacciPivotPoint,CamrillaPivotPoint
from .serializers import PivotPointModelSerializer,FibonacciPivotPointSerializer,CamarillaPivotPointSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Max
# Create your views here.

@api_view(['GET'])
def pivot_point_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = PivotPoint.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(script_name=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = PivotPointModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)
        

@api_view(['GET'])
def fibonacci_pivot_point_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = FibonacciPivotPoint.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(script_name=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = FibonacciPivotPointSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def camarilla_pivot_point(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = CamrillaPivotPoint.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(script_name=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = CamarillaPivotPointSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)