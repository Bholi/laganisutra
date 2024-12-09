from django.urls import path
from .views import subindices_view
urlpatterns = [
    path('subindices/',subindices_view),
]