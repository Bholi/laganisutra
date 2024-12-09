from django.shortcuts import render
from .serializer import CandlesSerializer
from .models import CandlestickPattern
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def candle_view(request):
    if request.method == 'GET':
        # Get query parameters
        symbol = request.GET.get('symbol', None)
        date = request.GET.get('date', None)
        time = request.GET.get('time', None)

        # Start with all data
        queryset = CandlestickPattern.objects.all()

        # Apply filters dynamically
        if symbol:
            queryset = queryset.filter(symbol=symbol)
        if date:
            queryset = queryset.filter(date=date)
        if time:
            queryset = queryset.filter(time=time)

        # Serialize the filtered data
        serializer = CandlesSerializer(queryset, many=True)
        return Response(serializer.data)
