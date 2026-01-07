from django.shortcuts import render,redirect
from .forms import RegUser

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from .models import CustomUser

# Create your views here.



def homepage(request):
    return render(request,'homepage.html')

def buyer_register(request):
    if request.method == 'POST':
        form = RegUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect(loginpage)
    else:
        form = RegUser()  

    return render(request, 'register.html', {'form': form})


def seller_register(request):
    if request.method == 'POST':
        form = RegUser(request.POST)
        if form.is_valid():
            seller = form.save(commit=False)
            seller.role = 'seller'
            seller.save()
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







