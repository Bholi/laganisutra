from django.urls import path
from .views import get_recent_datetime_data
urlpatterns = [
    path('',get_recent_datetime_data),
]