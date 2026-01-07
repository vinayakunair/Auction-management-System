from django.urls import path
from .views import auction_list, auction_detail, seller_dashboard, create_auction, edit_auction, delete_auction

urlpatterns = [
    path('', auction_list, name='auction_list'),
    path('<int:pk>/', auction_detail, name='auction_detail'),
    path('seller/dashboard/', seller_dashboard, name='seller_dashboard'),
    path('seller/create/', create_auction, name='create_auction'),
    path('seller/edit/<int:pk>/',edit_auction, name='edit_auction'),
    path('seller/delete/<int:pk>/', delete_auction, name='delete_auction'),
]

