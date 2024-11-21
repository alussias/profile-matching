from django.urls import path
from . import views

urlpatterns = [
    # Halaman dashboard utama
    path('', views.dashboard, name='dashboard'),
    
    # Halaman profil ideal
    path('ideal-profil/', views.ideal_profil, name='ideal-profil'),
    
    # Halaman hasil perhitungan
    path('result/', views.result, name='result'),
    
    # Endpoint untuk menyimpan hasil perhitungan
    path('result/store/', views.store_result, name='store-result'),
    
    # Endpoint untuk menyimpan ranking
    path('result/store-rank/', views.store_rank, name='store-rank'),
]