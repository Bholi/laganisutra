from rest_framework.decorators import api_view
from rest_framework.response import Response
from livedata.models import LiveFeedData
from django.db.models import Max, FloatField
from django.db.models.functions import Cast,Abs
from datetime import timedelta

@api_view(['GET'])
def top_gainers(request):
    try:
        # Find the latest date in the database
        latest_datetime = LiveFeedData.objects.aggregate(latest=Max('datetime'))['latest']

        if not latest_datetime:
            return Response({"message": "No data available"}, status=200)

        # Filter data for the latest date
        latest_day_start = latest_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        latest_day_end = latest_day_start + timedelta(days=1)

        last_day_data = LiveFeedData.objects.filter(datetime__gte=latest_day_start, datetime__lt=latest_day_end)

        # Convert percent_change to float and sort by top gainers
        top_gainers = last_day_data.annotate(
            percent_change_float=Cast('percent_change', FloatField())
        ).order_by('-percent_change_float')[:10]

        # Prepare response data
        response_data = [
            {
                # "datetime":data.datetime,
                "symbol": data.symbol,
                "ltp": data.ltp,
                "point_change": data.point_change,
                "percent_change": data.percent_change,
            }
            for data in top_gainers
        ]

        return Response({"top_gainers": response_data})

    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
def top_losers(request):
    try:
        # Find the latest date in the database
        latest_datetime = LiveFeedData.objects.aggregate(latest=Max('datetime'))['latest']

        if not latest_datetime:
            return Response({"message": "No data available"}, status=404)

        # Filter data for the latest day
        latest_day_start = latest_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        latest_day_end = latest_day_start + timedelta(days=1)

        last_day_data = LiveFeedData.objects.filter(datetime__gte=latest_day_start, datetime__lt=latest_day_end)

        # Convert percent_change to float and sort by top losers
        top_losers = last_day_data.annotate(
            percent_change_float=Cast('percent_change', FloatField())
        ).order_by('percent_change_float')[:10]

        # Prepare response data
        response_data = [
            {
                "symbol": data.symbol,
                "ltp": data.ltp,
                "point_change": data.point_change,
                "percent_change": data.percent_change,
            }
            for data in top_losers
        ]

        return Response({"top_losers": response_data})

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    

@api_view(['GET'])
def top_volume(request):
    try:
        # Find the latest date in the database
        latest_datetime = LiveFeedData.objects.aggregate(latest=Max('datetime'))['latest']

        if not latest_datetime:
            return Response({"message": "No data available"}, status=404)

        # Filter data for the latest day
        latest_day_start = latest_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        latest_day_end = latest_day_start + timedelta(days=1)

        last_day_data = LiveFeedData.objects.filter(datetime__gte=latest_day_start, datetime__lt=latest_day_end)

        # Convert volume to float and sort by top volume
        top_volume = last_day_data.annotate(
            volume_float=Cast('volume', FloatField())
        ).order_by('-volume_float')[:10]

        # Prepare response data
        response_data = [
            {
                "symbol": data.symbol,
                "ltp": data.ltp,
                # "point_change": data.point_change,
                # "percent_change": data.percent_change,
                "volume": data.volume,
            }
            for data in top_volume
        ]

        return Response({"top_volume": response_data})

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['GET'])
def top_fluctuating(request):
    try:
        # Find the latest date in the database
        latest_datetime = LiveFeedData.objects.aggregate(latest=Max('datetime'))['latest']

        if not latest_datetime:
            return Response({"message": "No data available"}, status=404)

        # Filter data for the latest day
        latest_day_start = latest_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        latest_day_end = latest_day_start + timedelta(days=1)

        last_day_data = LiveFeedData.objects.filter(datetime__gte=latest_day_start, datetime__lt=latest_day_end)

        # Convert point_change to float and calculate absolute value for fluctuation
        top_fluctuating = last_day_data.annotate(
            point_change_float=Cast('point_change', FloatField()),
            abs_fluctuation=Abs(Cast('point_change', FloatField()))
        ).order_by('-abs_fluctuation')[:10]

        # Prepare response data
        response_data = [
            {
                "symbol": data.symbol,
                "ltp": data.ltp,
                "point_change": data.point_change,
                "percent_change": data.percent_change,
            }
            for data in top_fluctuating
        ]

        return Response({"top_fluctuating": response_data})

    except Exception as e:
        return Response({"error": str(e)}, status=500)