from django.shortcuts import render,redirect
from .forms import RegUser

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from .models import CustomUser

# Create your views here.



from auctions.models import AuctionItem

def homepage(request):
    auctions = AuctionItem.objects.filter(is_active=True)
    return render(request, 'homepage.html', {'auctions': auctions})


def register(request):
    if request.method == 'POST':
        form = RegUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect(loginpage)
    else:
        form = RegUser()

    return render(request, 'register.html', {'form': form})








def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print("USERNAME =", username)
        print("PASSWORD =", password)

        user = authenticate(request, username=username, password=password)
        print("AUTH USER =", user)

        if user is not None:
            login(request, user)
            return redirect('homepage')

    return render(request, 'login.html')







