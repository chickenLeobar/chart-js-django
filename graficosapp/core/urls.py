from django.conf.urls import url
from .views import Principal
from django.urls import path
from .views import JSONPieChart
urlpatterns = [
    path('', Principal.as_view(), name="graficos"),
    path('chartjs/<str:id>', JSONPieChart.as_view(), name="testchar")
]
