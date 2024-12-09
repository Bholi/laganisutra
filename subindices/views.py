from .models import SubIndices
from .serializer import SubIndicesSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['GET'])
def subindices_view(request):
    date = request.GET.get('date', None)
    # Initialize the queryset
    queryset = SubIndices.objects.all()

    if date:
        queryset = queryset.filter(date=date)
    # Serialize the data
    serializer = SubIndicesSerializer(queryset, many=True)
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)