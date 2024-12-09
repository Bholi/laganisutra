from django.urls import path
from .views import MarketCycleStageListView

urlpatterns=[
    path('market-cycle-stages/', MarketCycleStageListView.as_view(), name='market-cycle-stages'),
]