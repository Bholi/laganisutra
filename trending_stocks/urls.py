from django.urls import path
from . import views
urlpatterns=[
    path('top-gainers/',views.top_gainers),
    path('top-losers/',views.top_losers),
    path('top-volume/',views.top_volume),
    path('top-fluctuating/',views.top_fluctuating),
]