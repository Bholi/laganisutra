
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import TradeAnalysis,BoilerRoom,EmbezzlementData,LayeringSpoofingData,PonziSchemeData,RampingData,ThresholdTuningData,WashTradeData
from rest_framework import status
from rest_framework.response import Response
from .serializers import TradeAnalysisSerializer,BoilerRoomSerializer,EmbezzlementSerializer,LayeringSerializer,PonziSerializer,RampingSerializer,ThresholdSerializer,WashingSerializer
from rest_framework.decorators import api_view

class TradeAnalysisList(generics.ListAPIView):
    queryset = TradeAnalysis.objects.all()
    serializer_class = TradeAnalysisSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = [
        'symbol',
        'buyer',
        'seller',
        'repeated_trades_flag',
        'price_manipulation_flag',
        'painting_the_tape_flag',
        'volume_spike_flag',
        'circular_trading_flag',
        'pump_flag',
        'dump_flag',
        'seller_reappears_flag',
        'suspicious',
    ]
    ordering_fields = '__all__'  # Allow ordering on all fields


@api_view(['GET'])
def floorsheet_data_list(request):
    # Apply filtering
    queryset = BoilerRoom.objects.all()

    # Filtering based on query parameters
    symbol = request.GET.get('symbol', None)
    boiler_room_flag = request.GET.get('boiler_room_flag', None)

    if symbol:
        queryset = queryset.filter(symbol__icontains=symbol)

    if boiler_room_flag is not None:
        queryset = queryset.filter(boiler_room_flag=boiler_room_flag.lower() == 'true')

    serializer = BoilerRoomSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def embezzlement_data_list(request):
    # Apply filtering
    queryset = EmbezzlementData.objects.all()

    # Filtering based on query parameters
    symbol = request.GET.get('symbol', None)
    embezzlement_flag = request.GET.get('embezzlement_flag', None)
    transaction_no = request.GET.get('transaction_no', None)

    if symbol:
        queryset = queryset.filter(symbol__icontains=symbol)

    if embezzlement_flag is not None:
        queryset = queryset.filter(embezzlement_flag=embezzlement_flag.lower() == 'true')

    if transaction_no:
        queryset = queryset.filter(transaction_no__icontains=transaction_no)

    serializer = EmbezzlementSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def layering_spoofing_data_list(request):
    # Apply filtering
    queryset = LayeringSpoofingData.objects.all()

    # Filtering based on query parameters
    symbol = request.GET.get('symbol',None)
    transaction_no = request.GET.get('transaction_no', None)
    layering_flag = request.GET.get('layering_flag', None)
    spoofing_flag = request.GET.get('spoofing_flag', None)

    if symbol:
        queryset = queryset.filter(symbol__icontains=symbol)

    if transaction_no:
        queryset = queryset.filter(transaction_no__icontains=transaction_no)

    if layering_flag is not None:
        queryset = queryset.filter(layering_flag=layering_flag.lower() == 'true')

    if spoofing_flag is not None:
        queryset = queryset.filter(spoofing_flag=spoofing_flag.lower() == 'true')

    serializer = LayeringSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def ponzi_scheme_data_list(request):
    # Apply filtering
    queryset = PonziSchemeData.objects.all()

    # Filtering based on query parameters
    symbol = request.GET.get('symbol',None)
    transaction_no = request.GET.get('transaction_no', None)
    ponzi_flag = request.GET.get('ponzi_flag', None)

    if symbol:
        queryset = queryset.filter(symbol__icontains=symbol)

    if transaction_no:
        queryset = queryset.filter(transaction_no__icontains=transaction_no)

    if ponzi_flag is not None:
        queryset = queryset.filter(ponzi_flag=ponzi_flag.lower() == 'true')

    serializer = PonziSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def ramping_data_list(request):
    # Apply filtering
    queryset = RampingData.objects.all()

    # Filtering based on query parameters
    symbol = request.GET.get('symbol',None)
    transaction_no = request.GET.get('transaction_no', None)
    ramping_flag = request.GET.get('ramping_flag', None)

    if symbol:
        queryset = queryset.filter(symbol__icontains = symbol)

    if transaction_no:
        queryset = queryset.filter(transaction_no__icontains=transaction_no)

    if ramping_flag is not None:
        queryset = queryset.filter(ramping_flag=ramping_flag.lower() == 'true')

    serializer = RampingSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def threshold_tuning_data_list(request):
    queryset = ThresholdTuningData.objects.all()

    # Apply optional filters
    potential_anomaly = request.GET.get('potential_anomaly', None)
    buyer = request.GET.get('buyer', None)

    if potential_anomaly is not None:
        queryset = queryset.filter(potential_anomaly=potential_anomaly.lower() == 'true')

    if buyer:
        queryset = queryset.filter(buyer__icontains=buyer)

    serializer = ThresholdSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def wash_trade_list(request):
    queryset = WashTradeData.objects.all()

    # Optional filtering by symbol and wash trade flag
    symbol = request.GET.get('symbol', None)
    wash_trade = request.GET.get('wash_trade', None)

    if symbol:
        queryset = queryset.filter(symbol__icontains=symbol)

    if wash_trade is not None:
        queryset = queryset.filter(wash_trade_flag=wash_trade.lower() == 'true')

    serializer = WashingSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)