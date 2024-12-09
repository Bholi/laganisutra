from .models import RsiSummary,MacdSummary,AdxSummary,CciSummary,StochRsiSummary,WillRSummary,MomentumSummary,AoSummary,UoSummary,BopSummary,VwmaSummary
from momentum.models import RsiModel,MacdModel,AdxModel,CciData,StochasticRSI,WilliamPercentR,MomentumIndicator,AwesomeOscillator,UltimateOscillator,BopModel,VwmaModel
from .serializers import RsiSummaryModelSerializer,MacdSummaryModelSerializer,AdxSummaryModelSerializer,CciSummaryModelSerializer,StochRsiSummaryModelSerializer,MomentumSummaryModelSerializer,WillRSummaryModelSerializer,AoSummaryModelSerializer,UoSummaryModelSerializer,BopSummaryModelSerializer,VwmaSummaryModelSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

def update_rsi_summary():
    # Get distinct symbols and dates from RsiModel
    distinct_data = RsiModel.objects.values('symbol', 'date').distinct()

    # Loop through each distinct symbol and date
    for data in distinct_data:
        symbol = data['symbol']
        date = data['date']

        # Filter RsiModel for the given symbol and date
        rsi_entries = RsiModel.objects.filter(symbol=symbol, date=date)

        # Initialize counts
        positive_count = 0
        negative_count = 0
        neutral_count = 0

        # Count signals for the symbol and date
        for entry in rsi_entries:
            if entry.signal == 'Buy':
                positive_count += 1
            elif entry.signal == 'Sell':
                negative_count += 1
            elif entry.signal == 'Neutral':
                neutral_count += 1

        # Check if a summary for the symbol and date already exists
        summary, created = RsiSummary.objects.get_or_create(
            symbol=symbol, date=date,
            defaults={'positive': positive_count, 'negative': negative_count, 'neutral': neutral_count}
        )

        # If the summary already exists, update the counts
        if not created:
            summary.positive = positive_count
            summary.negative = negative_count
            summary.neutral = neutral_count
            summary.save()


@api_view(['GET'])
def get_rsi_summary(request):
    # Optionally filter by 'symbol' and/or 'date'
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Filter the queryset based on the provided query parameters
    if symbol and date:
        rsi_summary = RsiSummary.objects.filter(symbol=symbol, date=date)
    elif symbol:
        rsi_summary = RsiSummary.objects.filter(symbol=symbol)
    elif date:
        rsi_summary = RsiSummary.objects.filter(date=date)
    else:
        rsi_summary = RsiSummary.objects.all()

    # Serialize the data
    serializer = RsiSummaryModelSerializer(rsi_summary, many=True)
    return Response(serializer.data)


def update_macd_summary():
    # Get distinct symbols and dates from RsiModel
    distinct_data = MacdModel.objects.values('symbol', 'date').distinct()

    # Loop through each distinct symbol and date
    for data in distinct_data:
        symbol = data['symbol']
        date = data['date']

        # Filter RsiModel for the given symbol and date
        macd_entries = MacdModel.objects.filter(symbol=symbol, date=date)

        # Initialize counts
        positive_count = 0
        negative_count = 0
        neutral_count = 0

        # Count signals for the symbol and date
        for entry in macd_entries:
            if entry.signal == 'Buy':
                positive_count += 1
            elif entry.signal == 'Sell':
                negative_count += 1
            elif entry.signal == 'Neutral':
                neutral_count += 1

        # Check if a summary for the symbol and date already exists
        summary, created = MacdSummary.objects.get_or_create(
            symbol=symbol, date=date,
            defaults={'positive': positive_count, 'negative': negative_count, 'neutral': neutral_count}
        )

        # If the summary already exists, update the counts
        if not created:
            summary.positive = positive_count
            summary.negative = negative_count
            summary.neutral = neutral_count
            summary.save()

@api_view(['GET'])
def get_macd_summary(request):
    # Optionally filter by 'symbol' and/or 'date'
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Filter the queryset based on the provided query parameters
    if symbol and date:
        macd_summary = MacdSummary.objects.filter(symbol=symbol, date=date)
    elif symbol:
        macd_summary = MacdSummary.objects.filter(symbol=symbol)
    elif date:
        macd_summary = MacdSummary.objects.filter(date=date)
    else:
        macd_summary = MacdSummary.objects.all()

    # Serialize the data
    serializer = MacdSummaryModelSerializer(macd_summary, many=True)
    return Response(serializer.data)


def update_adx_summary():
    # Get distinct symbols and dates from RsiModel
    distinct_data = AdxModel.objects.values('symbol', 'date').distinct()

    # Loop through each distinct symbol and date
    for data in distinct_data:
        symbol = data['symbol']
        date = data['date']

        # Filter RsiModel for the given symbol and date
        adx_entries = AdxModel.objects.filter(symbol=symbol, date=date)

        # Initialize counts
        positive_count = 0
        negative_count = 0
        neutral_count = 0

        # Count signals for the symbol and date
        for entry in adx_entries:
            if entry.signal == 'Buy':
                positive_count += 1
            elif entry.signal == 'Sell':
                negative_count += 1
            elif entry.signal == 'Neutral':
                neutral_count += 1

        # Check if a summary for the symbol and date already exists
        summary, created = AdxSummary.objects.get_or_create(
            symbol=symbol, date=date,
            defaults={'positive': positive_count, 'negative': negative_count, 'neutral': neutral_count}
        )

        # If the summary already exists, update the counts
        if not created:
            summary.positive = positive_count
            summary.negative = negative_count
            summary.neutral = neutral_count
            summary.save()

@api_view(['GET'])
def get_adx_summary(request):
    # Optionally filter by 'symbol' and/or 'date'
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Filter the queryset based on the provided query parameters
    if symbol and date:
        adx_summary = AdxSummary.objects.filter(symbol=symbol, date=date)
    elif symbol:
        adx_summary = AdxSummary.objects.filter(symbol=symbol)
    elif date:
        adx_summary = AdxSummary.objects.filter(date=date)
    else:
        adx_summary = AdxSummary.objects.all()

    # Serialize the data
    serializer = AdxSummaryModelSerializer(adx_summary, many=True)
    return Response(serializer.data)

def update_cci_summary():
    # Get distinct symbols and dates from RsiModel
    distinct_data = CciData.objects.values('script_name', 'date').distinct()

    # Loop through each distinct symbol and date
    for data in distinct_data:
        symbol = data['script_name']
        date = data['date']

        # Filter RsiModel for the given symbol and date
        cci_entries = CciData.objects.filter(script_name=symbol, date=date)

        # Initialize counts
        positive_count = 0
        negative_count = 0
        neutral_count = 0

        # Count signals for the symbol and date
        for entry in cci_entries:
            if entry.signal == 'Buy':
                positive_count += 1
            elif entry.signal == 'Sell':
                negative_count += 1
            elif entry.signal == 'Neutral':
                neutral_count += 1

        # Check if a summary for the symbol and date already exists
        summary, created = CciSummary.objects.get_or_create(
            symbol=symbol, date=date,
            defaults={'positive': positive_count, 'negative': negative_count, 'neutral': neutral_count}
        )

        # If the summary already exists, update the counts
        if not created:
            summary.positive = positive_count
            summary.negative = negative_count
            summary.neutral = neutral_count
            summary.save()

@api_view(['GET'])
def get_cci_summary(request):
    # Optionally filter by 'symbol' and/or 'date'
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Filter the queryset based on the provided query parameters
    if symbol and date:
        cci_summary = CciSummary.objects.filter(symbol=symbol, date=date)
    elif symbol:
        cci_summary = CciSummary.objects.filter(symbol=symbol)
    elif date:
        cci_summary = CciSummary.objects.filter(date=date)
    else:
        cci_summary = CciSummary.objects.all()

    # Serialize the data
    serializer = CciSummaryModelSerializer(cci_summary, many=True)
    return Response(serializer.data)


def update_ao_summary():
    # Get distinct symbols and dates from RsiModel
    distinct_data = AwesomeOscillator.objects.values('script_name', 'date').distinct()

    # Loop through each distinct symbol and date
    for data in distinct_data:
        symbol = data['script_name']
        date = data['date']

        # Filter RsiModel for the given symbol and date
        cci_entries = AwesomeOscillator.objects.filter(script_name=symbol, date=date)

        # Initialize counts
        positive_count = 0
        negative_count = 0
        neutral_count = 0

        # Count signals for the symbol and date
        for entry in cci_entries:
            if entry.signal == 'Buy':
                positive_count += 1
            elif entry.signal == 'Sell':
                negative_count += 1
            elif entry.signal == 'Neutral':
                neutral_count += 1

        # Check if a summary for the symbol and date already exists
        summary, created = AoSummary.objects.get_or_create(
            symbol=symbol, date=date,
            defaults={'positive': positive_count, 'negative': negative_count, 'neutral': neutral_count}
        )

        # If the summary already exists, update the counts
        if not created:
            summary.positive = positive_count
            summary.negative = negative_count
            summary.neutral = neutral_count
            summary.save()

@api_view(['GET'])
def get_ao_summary(request):
    # Optionally filter by 'symbol' and/or 'date'
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Filter the queryset based on the provided query parameters
    if symbol and date:
        ao_summary = AoSummary.objects.filter(symbol=symbol, date=date)
    elif symbol:
        ao_summary = AoSummary.objects.filter(symbol=symbol)
    elif date:
        ao_summary = AoSummary.objects.filter(date=date)
    else:
        ao_summary = AoSummary.objects.all()

    # Serialize the data
    serializer = AoSummaryModelSerializer(ao_summary, many=True)
    return Response(serializer.data)


def update_stoch_summary():
    # Get distinct symbols and dates from RsiModel
    distinct_data = StochasticRSI.objects.values('symbol', 'date').distinct()

    # Loop through each distinct symbol and date
    for data in distinct_data:
        symbol = data['symbol']
        date = data['date']

        # Filter RsiModel for the given symbol and date
        stoch_entries = StochasticRSI.objects.filter(symbol=symbol, date=date)

        # Initialize counts
        positive_count = 0
        negative_count = 0
        neutral_count = 0

        # Count signals for the symbol and date
        for entry in stoch_entries:
            if entry.signal == 'Buy':
                positive_count += 1
            elif entry.signal == 'Sell':
                negative_count += 1
            elif entry.signal == 'Neutral':
                neutral_count += 1

        # Check if a summary for the symbol and date already exists
        summary, created = StochRsiSummary.objects.get_or_create(
            symbol=symbol, date=date,
            defaults={'positive': positive_count, 'negative': negative_count, 'neutral': neutral_count}
        )

        # If the summary already exists, update the counts
        if not created:
            summary.positive = positive_count
            summary.negative = negative_count
            summary.neutral = neutral_count
            summary.save()

@api_view(['GET'])
def get_stoch_summary(request):
    # Optionally filter by 'symbol' and/or 'date'
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Filter the queryset based on the provided query parameters
    if symbol and date:
        stoch_summary = StochRsiSummary.objects.filter(symbol=symbol, date=date)
    elif symbol:
        stoch_summary = StochRsiSummary.objects.filter(symbol=symbol)
    elif date:
        stoch_summary = StochRsiSummary.objects.filter(date=date)
    else:
        stoch_summary = StochRsiSummary.objects.all()

    # Serialize the data
    serializer = StochRsiSummaryModelSerializer(stoch_summary, many=True)
    return Response(serializer.data)



def update_willr_summary():
    # Get distinct symbols and dates from RsiModel
    distinct_data = WilliamPercentR.objects.values('symbol', 'date').distinct()

    # Loop through each distinct symbol and date
    for data in distinct_data:
        symbol = data['symbol']
        date = data['date']

        # Filter RsiModel for the given symbol and date
        willr_entries = WilliamPercentR.objects.filter(symbol=symbol, date=date)

        # Initialize counts
        positive_count = 0
        negative_count = 0
        neutral_count = 0

        # Count signals for the symbol and date
        for entry in willr_entries:
            if entry.signal == 'Buy':
                positive_count += 1
            elif entry.signal == 'Sell':
                negative_count += 1
            elif entry.signal == 'Neutral':
                neutral_count += 1

        # Check if a summary for the symbol and date already exists
        summary, created = WillRSummary.objects.get_or_create(
            symbol=symbol, date=date,
            defaults={'positive': positive_count, 'negative': negative_count, 'neutral': neutral_count}
        )

        # If the summary already exists, update the counts
        if not created:
            summary.positive = positive_count
            summary.negative = negative_count
            summary.neutral = neutral_count
            summary.save()

@api_view(['GET'])
def get_willr_summary(request):
    # Optionally filter by 'symbol' and/or 'date'
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Filter the queryset based on the provided query parameters
    if symbol and date:
        willr_summary = WillRSummary.objects.filter(symbol=symbol, date=date)
    elif symbol:
        willr_summary = WillRSummary.objects.filter(symbol=symbol)
    elif date:
        willr_summary = WillRSummary.objects.filter(date=date)
    else:
        willr_summary = WillRSummary.objects.all()

    # Serialize the data
    serializer = WillRSummaryModelSerializer(willr_summary, many=True)
    return Response(serializer.data)


def update_mom_summary():
    # Get distinct symbols and dates from RsiModel
    distinct_data = MomentumIndicator.objects.values('symbol', 'date').distinct()

    # Loop through each distinct symbol and date
    for data in distinct_data:
        symbol = data['symbol']
        date = data['date']

        # Filter RsiModel for the given symbol and date
        mom_entries = MomentumIndicator.objects.filter(symbol=symbol, date=date)

        # Initialize counts
        positive_count = 0
        negative_count = 0
        neutral_count = 0

        # Count signals for the symbol and date
        for entry in mom_entries:
            if entry.signal == 'Buy':
                positive_count += 1
            elif entry.signal == 'Sell':
                negative_count += 1
            elif entry.signal == 'Neutral':
                neutral_count += 1

        # Check if a summary for the symbol and date already exists
        summary, created = MomentumSummary.objects.get_or_create(
            symbol=symbol, date=date,
            defaults={'positive': positive_count, 'negative': negative_count, 'neutral': neutral_count}
        )

        # If the summary already exists, update the counts
        if not created:
            summary.positive = positive_count
            summary.negative = negative_count
            summary.neutral = neutral_count
            summary.save()


@api_view(['GET'])
def get_mom_summary(request):
    # Optionally filter by 'symbol' and/or 'date'
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Filter the queryset based on the provided query parameters
    if symbol and date:
        mom_summary = MomentumSummary.objects.filter(symbol=symbol, date=date)
    elif symbol:
        mom_summary = MomentumSummary.objects.filter(symbol=symbol)
    elif date:
        mom_summary = MomentumSummary.objects.filter(date=date)
    else:
        mom_summary = MomentumSummary.objects.all()

    # Serialize the data
    serializer = MomentumSummaryModelSerializer(mom_summary, many=True)
    return Response(serializer.data)



def update_uo_summary():
    # Get distinct symbols and dates from RsiModel
    distinct_data = UltimateOscillator.objects.values('symbol', 'date').distinct()

    # Loop through each distinct symbol and date
    for data in distinct_data:
        symbol = data['symbol']
        date = data['date']

        # Filter RsiModel for the given symbol and date
        uo_entries = UltimateOscillator.objects.filter(symbol=symbol, date=date)

        # Initialize counts
        positive_count = 0
        negative_count = 0
        neutral_count = 0

        # Count signals for the symbol and date
        for entry in uo_entries:
            if entry.signal == 'Buy':
                positive_count += 1
            elif entry.signal == 'Sell':
                negative_count += 1
            elif entry.signal == 'Neutral':
                neutral_count += 1

        # Check if a summary for the symbol and date already exists
        summary, created = UoSummary.objects.get_or_create(
            symbol=symbol, date=date,
            defaults={'positive': positive_count, 'negative': negative_count, 'neutral': neutral_count}
        )

        # If the summary already exists, update the counts
        if not created:
            summary.positive = positive_count
            summary.negative = negative_count
            summary.neutral = neutral_count
            summary.save()


@api_view(['GET'])
def get_uo_summary(request):
    # Optionally filter by 'symbol' and/or 'date'
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Filter the queryset based on the provided query parameters
    if symbol and date:
        uo_summary = UoSummary.objects.filter(symbol=symbol, date=date)
    elif symbol:
        uo_summary = UoSummary.objects.filter(symbol=symbol)
    elif date:
        uo_summary = UoSummary.objects.filter(date=date)
    else:
        uo_summary = UoSummary.objects.all()

    # Serialize the data
    serializer = UoSummaryModelSerializer(uo_summary, many=True)
    return Response(serializer.data)



def update_bop_summary():
    # Get distinct symbols and dates from RsiModel
    distinct_data = BopModel.objects.values('symbol', 'date').distinct()

    # Loop through each distinct symbol and date
    for data in distinct_data:
        symbol = data['symbol']
        date = data['date']

        # Filter RsiModel for the given symbol and date
        bop_entries = BopModel.objects.filter(symbol=symbol, date=date)

        # Initialize counts
        positive_count = 0
        negative_count = 0
        neutral_count = 0

        # Count signals for the symbol and date
        for entry in bop_entries:
            if entry.signal == 'Buy':
                positive_count += 1
            elif entry.signal == 'Sell':
                negative_count += 1
            elif entry.signal == 'Neutral':
                neutral_count += 1

        # Check if a summary for the symbol and date already exists
        summary, created = BopSummary.objects.get_or_create(
            symbol=symbol, date=date,
            defaults={'positive': positive_count, 'negative': negative_count, 'neutral': neutral_count}
        )

        # If the summary already exists, update the counts
        if not created:
            summary.positive = positive_count
            summary.negative = negative_count
            summary.neutral = neutral_count
            summary.save()


@api_view(['GET'])
def get_bop_summary(request):
    # Optionally filter by 'symbol' and/or 'date'
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Filter the queryset based on the provided query parameters
    if symbol and date:
        bop_summary = BopSummary.objects.filter(symbol=symbol, date=date)
    elif symbol:
        bop_summary = BopSummary.objects.filter(symbol=symbol)
    elif date:
        bop_summary = BopSummary.objects.filter(date=date)
    else:
        bop_summary = BopSummary.objects.all()

    # Serialize the data
    serializer = BopSummaryModelSerializer(bop_summary, many=True)
    return Response(serializer.data)


def update_vwma_summary():
    # Get distinct symbols and dates from RsiModel
    distinct_data = VwmaModel.objects.values('symbol', 'date').distinct()

    # Loop through each distinct symbol and date
    for data in distinct_data:
        symbol = data['symbol']
        date = data['date']

        # Filter RsiModel for the given symbol and date
        vwma_entries = VwmaModel.objects.filter(symbol=symbol, date=date)

        # Initialize counts
        positive_count = 0
        negative_count = 0
        neutral_count = 0

        # Count signals for the symbol and date
        for entry in vwma_entries:
            if entry.signal == 'Buy':
                positive_count += 1
            elif entry.signal == 'Sell':
                negative_count += 1
            elif entry.signal == 'Neutral':
                neutral_count += 1

        # Check if a summary for the symbol and date already exists
        summary, created = VwmaSummary.objects.get_or_create(
            symbol=symbol, date=date,
            defaults={'positive': positive_count, 'negative': negative_count, 'neutral': neutral_count}
        )

        # If the summary already exists, update the counts
        if not created:
            summary.positive = positive_count
            summary.negative = negative_count
            summary.neutral = neutral_count
            summary.save()


@api_view(['GET'])
def get_vwma_summary(request):
    # Optionally filter by 'symbol' and/or 'date'
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Filter the queryset based on the provided query parameters
    if symbol and date:
        vwma_summary = VwmaSummary.objects.filter(symbol=symbol, date=date)
    elif symbol:
        vwma_summary = VwmaSummary.objects.filter(symbol=symbol)
    elif date:
        vwma_summary = VwmaSummary.objects.filter(date=date)
    else:
        vwma_summary = VwmaSummary.objects.all()

    # Serialize the data
    serializer = VwmaSummaryModelSerializer(vwma_summary, many=True)
    return Response(serializer.data)
