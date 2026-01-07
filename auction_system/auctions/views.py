from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

def auction_list(request):
    return render(request, 'auction_list.html')
