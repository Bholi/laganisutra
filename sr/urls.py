from django.urls import path
from .views import SupportResistanceView

urlpatterns = [
    path('support-resistance/', SupportResistanceView.as_view(), name='support_resistance_api'),
]