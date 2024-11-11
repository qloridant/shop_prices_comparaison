# main/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('search/', views.search_supermarkets, name='search_supermarkets'),
    path('select_supermarket/', views.select_supermarket, name='select_supermarket'),
    path('compare/', views.shops_compare_summary, name='compare'),
]