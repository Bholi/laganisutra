
from .models import AllScriptsData
from .serializers import AllScriptsDataSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.dateparse import parse_date

# Create your views here.

# @api_view(['GET'])
# def alldata_view(request):
#     if request.method == 'GET':
#         all_data = AllScriptsData.objects.all()
#         serailizer = AllScriptsDataSerializer(all_data,many=True)
#         return Response(serailizer.data)

# @api_view(['GET'])
# def alldata_view(request):
#     if request.method == 'GET':
#         # Get the 'symbol' parameter from the query params (if provided)
#         symbol = request.GET.get('symbol', None)
        
#         # Filter the data by symbol if provided
#         if symbol:
#             all_data = AllScriptsData.objects.filter(symbol=symbol)
#         else:
#             all_data = AllScriptsData.objects.all()

#         # Serialize the filtered data
#         serializer = AllScriptsDataSerializer(all_data, many=True)
#         return Response(serializer.data)


@api_view(['GET'])
def alldata_view(request):
    if request.method == 'GET':
        # Get the 'symbol', 'start_date', and 'end_date' query parameters (if provided)
        symbol = request.GET.get('symbol', None)
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        
        # Parse the start_date and end_date to date objects
        if start_date:
            start_date = parse_date(start_date)
        if end_date:
            end_date = parse_date(end_date)
        
        # Filter data based on symbol, if provided
        if symbol:
            all_data = AllScriptsData.objects.filter(symbol=symbol)
        else:
            all_data = AllScriptsData.objects.all()
        
        # Apply date range filter if both start_date and end_date are provided
        if start_date and end_date:
            all_data = all_data.filter(date__range=[start_date, end_date])
        elif start_date:  # Apply only start_date if provided
            all_data = all_data.filter(date__gte=start_date)
        elif end_date:  # Apply only end_date if provided
            all_data = all_data.filter(date__lte=end_date)

        # Serialize the filtered data
        serializer = AllScriptsDataSerializer(all_data, many=True)
        return Response(serializer.data)
