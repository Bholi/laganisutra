from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import LiveFeedData
from .serializers import LiveDataSerializer
from django.db.models import Max


# @api_view(['GET'])
# def get_data(request):
#     try:
#         symbol = request.GET.get('symbol', None)
#         if symbol:
#             all_data = LiveFeedData.objects.filter(symbol=symbol)
#         else:
#             all_data = LiveFeedData.objects.all()
#         serializer = LiveDataSerializer(all_data, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_recent_datetime_data(request):
    try:
        # Get the most recent datetime
        recent_datetime = LiveFeedData.objects.aggregate(recent_datetime=Max('datetime'))['recent_datetime']

        # Filter records with the most recent datetime
        if recent_datetime:
            recent_data = LiveFeedData.objects.filter(datetime=recent_datetime)
        else:
            return Response({"message": "No data available"}, status=status.HTTP_200_OK)

        # Serialize the data
        serializer = LiveDataSerializer(recent_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def post_data(request):
    serializer = LiveDataSerializer(data=request.data, many=True)  # Set many=True to accept a list of records
    if serializer.is_valid():
        serializer.save()  # Saves each item in the incoming data list to the database
        return Response({"message": "Data saved successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)