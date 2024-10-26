# main/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_compare_summary, name='shop_summary'),  # Root URL for the combined view
]