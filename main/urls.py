# main/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_supermarkets, name='search_supermarkets'),
    path('select_supermarket/', views.select_supermarket, name='select_supermarket'),
    path('summary/', views.summary_selection, name='summary_selection'),
]