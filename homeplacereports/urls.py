from django.urls import path
from .views import SwapperPropertyList

urlpatterns = [
    path('reports/swapperproperties', SwapperPropertyList.as_view()),
]