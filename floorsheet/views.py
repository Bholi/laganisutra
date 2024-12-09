from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import FloorSheetData,StockSummaryReport,BuyerActivityReport,SellerActivityReport,HighValueTransactionReport,VolatilityAnalysisReport,TradeVolAnalysisReport,PriceMovementAnalysisReport,LiquidityConcentrationReport,PriceVolatilityVolumeReport,PriceElasticityDemandReport,StockPriceRangeReport,BrokerVolumeConcentrationReport,Sector
from .serializers import FloorSheetDataSerializer,StockSummaryReportSerializer,BuyerActivityReportSerializer,SellerActivityReportSerializer,HighValueReportSerializer,VolatilityAnalysisReportSerializer,TradeVolumeAnalysisReportSerializer,PriceMovementAnalysisReportSerializer,LCRReportSerializer,PVVRSerializer,PriceElasticitySerializer,StockPriceRangeReportSerializer,BrokerVolumeConcReportSerializer,SectorSerializer
from django.db.models import Max
from .pagination import DynamicPageSizePagination
from datetime import datetime


class FloorSheetDataView(APIView):
    def get(self, request):
        # Get query parameters for filtering
        symbol = request.GET.get('symbol')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        date = request.GET.get('date')

        # Filter the queryset based on the query parameters
        queryset = FloorSheetData.objects.all()
		
        if symbol:
            queryset = queryset.filter(symbol__iexact=symbol)  # Case-insensitive exact match for symbol
        if date:
            queryset = queryset.filter(date__iexact=date)

        if start_date and end_date:
            # Convert string dates to datetime objects
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                # Filter by date range
                queryset = queryset.filter(date__range=[start_date, end_date])
            except ValueError:
                return Response({"error": "Invalid date format. Please use 'YYYY-MM-DD' format."}, status=status.HTTP_400_BAD_REQUEST)

        elif start_date:  # If only start_date is provided
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                queryset = queryset.filter(date__gte=start_date)
            except ValueError:
                return Response({"error": "Invalid start_date format. Please use 'YYYY-MM-DD' format."}, status=status.HTTP_400_BAD_REQUEST)

        elif end_date:  # If only end_date is provided
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                queryset = queryset.filter(date__lte=end_date)
            except ValueError:
                return Response({"error": "Invalid end_date format. Please use 'YYYY-MM-DD' format."}, status=status.HTTP_400_BAD_REQUEST)

        # Apply pagination
        paginator = DynamicPageSizePagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        # Serialize and return paginated data
        serializer = FloorSheetDataSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)



        
@api_view(['POST'])
def receive_floorsheet_data(request):
    # Deserialize and validate the incoming data
    serializer = FloorSheetDataSerializer(data=request.data, many=True)

    if serializer.is_valid():
        # Filter out records already in the database
        new_data = []
        for item in serializer.validated_data:
            # Assuming `unique_field` is the field that identifies uniqueness
            if not FloorSheetData.objects.filter(transaction_no=item['transaction_no']).exists():
                new_data.append(item)

        if new_data:
            # Save only new data
            FloorSheetData.objects.bulk_create(
                [FloorSheetData(**data) for data in new_data]
            )
            return Response(
                {"message": f"{len(new_data)} new records successfully saved to the database."},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"message": "No new records to save."},
                status=status.HTTP_200_OK
            )
    else:
        return Response(
            {"message": "Failed to save data to the database.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
def get_stock_summary_report_data(request):
    # Fetch all aggregated floor sheet data
    aggregated_data = StockSummaryReport.objects.all()

    # Serialize the data
    serializer = StockSummaryReportSerializer(aggregated_data, many=True)

    # Return the serialized data as a JSON response
    return Response(serializer.data)


@api_view(['GET'])
def get_buyer_activity_report(request):
    # Fetch the latest date using Max
    latest_date = BuyerActivityReport.objects.aggregate(latest_date=Max('date'))['latest_date']

    if latest_date:
        # Filter data by the latest date and order by total_amount_spent in descending order
        buyer_activity_data = BuyerActivityReport.objects.filter(date=latest_date).order_by('-total_amount_spent')

        # Serialize the data
        serializer = BuyerActivityReportSerializer(buyer_activity_data, many=True)

        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "No data available for the latest date."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_all_buyer_activity_reports(request):
    # Delete all buyer activity reports
    deleted_count, _ = BuyerActivityReport.objects.all().delete()

    if deleted_count:
        return Response({"detail": f"{deleted_count} records deleted."}, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "No records found to delete."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_seller_activity_report(request):
    # Fetch the latest date using Max
    latest_date = SellerActivityReport.objects.aggregate(latest_date=Max('date'))['latest_date']

    if latest_date:
        # Filter data by the latest date and order by total_amount_received in descending order
        seller_activity_data = SellerActivityReport.objects.filter(date=latest_date).order_by('-total_amount_received')

        # Serialize the data
        serializer = SellerActivityReportSerializer(seller_activity_data, many=True)

        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "No data available for the latest date."}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE'])
def delete_all_seller_activity_reports(request):
    # Delete all buyer activity reports
    deleted_count, _ = SellerActivityReport.objects.all().delete()

    if deleted_count:
        return Response({"detail": f"{deleted_count} records deleted."}, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "No records found to delete."}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def get_high_value_transaction_report(request):
    # Fetch the latest date using Max
    latest_date = HighValueTransactionReport.objects.aggregate(latest_date=Max('date'))['latest_date']

    if latest_date:
        # Filter data by the latest date and order by total_amount_received in descending order
        high_value_data = HighValueTransactionReport.objects.filter(date=latest_date)

        # Serialize the data
        serializer = HighValueReportSerializer(high_value_data, many=True)

        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "No data available for the latest date."}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_volatility_analysis_report(request):
    # Fetch the latest date using Max
    latest_date = VolatilityAnalysisReport.objects.aggregate(latest_date=Max('date'))['latest_date']

    if latest_date:
        # Filter data by the latest date and order by total_amount_received in descending order
        volatiltiy_analysis_data = VolatilityAnalysisReport.objects.filter(date=latest_date)

        # Serialize the data
        serializer = VolatilityAnalysisReportSerializer(volatiltiy_analysis_data, many=True)

        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "No data available for the latest date."}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_trade_vol_analysis_report(request):
    # Fetch the latest date using Max
    latest_date = TradeVolAnalysisReport.objects.aggregate(latest_date=Max('date'))['latest_date']

    if latest_date:
        # Filter data by the latest date and order by total_amount_received in descending order
        tradevol_analysis_data = TradeVolAnalysisReport.objects.filter(date=latest_date)

        # Serialize the data
        serializer = TradeVolumeAnalysisReportSerializer(tradevol_analysis_data, many=True)

        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "No data available for the latest date."}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['DELETE'])
def delete_all_tradevol_activity_reports(request):
    # Delete all buyer activity reports
    deleted_count, _ = TradeVolAnalysisReport.objects.all().delete()

    if deleted_count:
        return Response({"detail": f"{deleted_count} records deleted."}, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "No records found to delete."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_price_movement_analysis_report(request):
    # Fetch the latest date using Max
    latest_date = PriceMovementAnalysisReport.objects.aggregate(latest_date=Max('date'))['latest_date']

    if latest_date:
        # Filter data by the latest date and order by total_amount_received in descending order
        pricemovement_analysis_data = PriceMovementAnalysisReport.objects.filter(date=latest_date)

        # Serialize the data
        serializer = PriceMovementAnalysisReportSerializer(pricemovement_analysis_data, many=True)

        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "No data available for the latest date."}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def get_lcr_analysis_report(request):
    # Fetch the latest date using Max
    latest_date = LiquidityConcentrationReport.objects.aggregate(latest_date=Max('date'))['latest_date']

    if latest_date:
        # Filter data by the latest date and order by total_amount_received in descending order
        lcr_analysis_data = LiquidityConcentrationReport.objects.filter(date=latest_date)

        # Serialize the data
        serializer = LCRReportSerializer(lcr_analysis_data, many=True)

        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "No data available for the latest date."}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_pvvr_analysis_report(request):
    # Fetch the latest date using Max
    latest_date = PriceVolatilityVolumeReport.objects.aggregate(latest_date=Max('date'))['latest_date']

    if latest_date:
        # Filter data by the latest date and order by total_amount_received in descending order
        pvvr_data = PriceVolatilityVolumeReport.objects.filter(date=latest_date)

        # Serialize the data
        serializer = PVVRSerializer(pvvr_data, many=True)

        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "No data available for the latest date."}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_price_elasticity_analysis_report(request):
    # Fetch the latest date using Max
    latest_date = PriceElasticityDemandReport.objects.aggregate(latest_date=Max('date'))['latest_date']

    if latest_date:
        # Filter data by the latest date and order by total_amount_received in descending order
        price_elasticity_data = PriceElasticityDemandReport.objects.filter(date=latest_date)

        # Serialize the data
        serializer = PriceElasticitySerializer(price_elasticity_data, many=True)

        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "No data available for the latest date."}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_stock_price_range_report(request):
    # Fetch the latest date using Max
    latest_date = StockPriceRangeReport.objects.aggregate(latest_date=Max('date'))['latest_date']

    if latest_date:
        # Filter data by the latest date and order by total_amount_received in descending order
        stock_price_range_data = StockPriceRangeReport.objects.filter(date=latest_date)

        # Serialize the data
        serializer = StockPriceRangeReportSerializer(stock_price_range_data, many=True)

        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "No data available for the latest date."}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_broker_volume_report(request):
    # Fetch the latest date using Max
    latest_date = BrokerVolumeConcentrationReport.objects.aggregate(latest_date=Max('date'))['latest_date']

    if latest_date:
        # Filter data by the latest date and order by total_amount_received in descending order
        broker_volume_data = BrokerVolumeConcentrationReport.objects.filter(date=latest_date)

        # Serialize the data
        serializer = BrokerVolumeConcReportSerializer(broker_volume_data, many=True)

        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "No data available for the latest date."}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def sectors_view(request):
    # Fetch the latest date using Max
    queryset = Sector.objects.all()
    if queryset:    # Serialize the data
        serializer = SectorSerializer(queryset, many=True)
        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "No data available for the latest date."}, status=status.HTTP_404_NOT_FOUND)
    