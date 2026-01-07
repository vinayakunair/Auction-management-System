from django.urls import path
from .views import*

from  django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('homep/', homepage, name='homepage'),
    path('regp/', buyer_register, name='buyer_register'),
    path('regsp/', seller_register, name='seller_register'),
    path('logp/', loginpage, name='login'),
]




urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)