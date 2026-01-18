from django.urls import path
from .views import *

urlpatterns = [
    
    path('auction/<int:pk>/status/', auction_status_api, name='auction_status_api'),

    path('<int:pk>/', auction_detail, name='auction_detail'),

    path('seller/dashboard/', seller_dashboard, name='seller_dashboard'),
    path('seller/create/', create_auction, name='create_auction'),
    path('seller/edit/<int:pk>/', edit_auction, name='edit_auction'),
    path('seller/delete/<int:pk>/', delete_auction, name='delete_auction'),
]
