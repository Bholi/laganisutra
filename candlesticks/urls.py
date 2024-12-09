from django.urls import path
from .views import candle_view
urlpatterns = [
    path('',candle_view)
]