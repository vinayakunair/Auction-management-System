from django.urls import path
from .views import auction_list

urlpatterns = [
    path('', auction_list, name='auction_list'),
]
