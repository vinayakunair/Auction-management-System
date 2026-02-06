from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', homepage, name='homepage'),
    path('logp/', loginpage, name='login'),
    path('regp/', register, name='register'),
    
    path('seller-register/', seller_register, name='seller_register'),
    path('logout/', logout_view, name='logout'),

    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/approve/<int:auction_id>/', approve_auction, name='approve_auction'),
    path('dashboard/disable/<int:auction_id>/', disable_auction, name='disable_auction'),
    path('dashboard/block/<int:user_id>/', block_user, name='block_user'),
    path('dashboard/unblock/<int:user_id>/', unblock_user, name='unblock_user'),
    path('buyer/dashboard/', buyer_dashboard, name='buyer_dashboard'),
    path('dashboard/users/', admin_users_list, name='admin_users_list'),
    path('dashboard/user/<int:user_id>/auctions/', admin_user_auctions, name='admin_user_auctions'),
    path('dashboard/seller/<int:seller_id>/auctions/', admin_seller_auctions, name='admin_seller_auctions'),
    path('password-reset/', password_reset_request, name='password_reset'),
    path('password-reset/verify/', password_reset_verify, name='password_reset_verify'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
