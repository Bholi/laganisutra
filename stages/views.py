from django.shortcuts import render
from .serializer import StagesSerializer
from .models import MarketCycleStage
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class MarketCycleStageListView(APIView):
    def get(self, request):
        symbol = request.query_params.get('symbol', None)
        if symbol:
            stages = MarketCycleStage.objects.filter(symbol=symbol)
        else:
            stages = MarketCycleStage.objects.all()

        # Serialize the data
        serializer = StagesSerializer(stages, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
