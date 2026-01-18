from django.urls import path
from .views import*

from  django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
    path('', loginpage, name='login'),
    path('regp/', register, name='register'),
    path('homep/', homepage, name='homepage'),
    path('seller-register/', seller_register, name='seller_register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/approve/<int:auction_id>/', approve_auction, name='approve_auction'),
    path('dashboard/disable/<int:auction_id>/', disable_auction, name='disable_auction'),

]




urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)