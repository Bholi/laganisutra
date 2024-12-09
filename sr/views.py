from django.shortcuts import render
from .serializer import SrSerializer
from .models import SupportResistance
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


class SupportResistanceView(APIView):
    """
    API endpoint to fetch support and resistance data.
    """

    def get(self, request):
        symbol = request.query_params.get('symbol', None)
        if symbol:
            data = SupportResistance.objects.filter(symbol=symbol)
        else:
            data = SupportResistance.objects.all()

        serializer = SrSerializer(data, many=True)
        return Response(serializer.data)


