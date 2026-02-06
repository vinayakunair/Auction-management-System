from django.urls import path
from .views import *

urlpatterns = [
    path('category/<slug:category>/', category_auctions, name='category_auctions'),
    path('auction/<int:pk>/status/', auction_status_api, name='auction_status_api'),
    path('seller/dashboard/', seller_dashboard, name='seller_dashboard'),
    path('seller/create/', create_auction, name='create_auction'),
    path('seller/edit/<int:pk>/', edit_auction, name='edit_auction'),
    path('seller/delete/<int:pk>/', delete_auction, name='delete_auction'),
    path('<int:pk>/', auction_detail, name='auction_detail'),
    path('seller/auction/<int:pk>/', seller_auction_detail, name='seller_auction_detail'),
    path('admin/delete/<int:pk>/', delete_auction_admin, name='delete_auction_admin'),
    path('admin/auction/<int:pk>/', admin_auction_detail, name='admin_auction_detail'),
]
