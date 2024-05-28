
from django.urls import path
from .views import DataCollectingView
  
urlpatterns = [
      path('datasorting/<str:product_name>/',DataCollectingView.as_view())
]
