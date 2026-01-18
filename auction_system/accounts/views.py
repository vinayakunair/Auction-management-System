from django.shortcuts import render,redirect
from .forms import RegUser,SellerRegisterForm

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from .models import CustomUser
from django.utils import timezone

from .decorators import admin_required
from auctions.models import AuctionItem, Bid
from django.contrib.auth import get_user_model


# Create your views here.

from django.shortcuts import get_object_or_404

@admin_required
def approve_auction(request, auction_id):
    auction = get_object_or_404(AuctionItem, id=auction_id)
    auction.is_active = True
    auction.save()
    return redirect('admin_dashboard')


@admin_required
def disable_auction(request, auction_id):
    auction = get_object_or_404(AuctionItem, id=auction_id)
    auction.is_active = False
    auction.save()
    return redirect('admin_dashboard')





def homepage(request):
    now = timezone.now()

    active_auctions = AuctionItem.objects.filter(
        is_active=True,
        start_time__lte=now,
        end_time__gte=now
    )

    ended_auctions = AuctionItem.objects.filter(
        end_time__lt=now
    )

    return render(request, 'homepage.html', {
        'active_auctions': active_auctions,
        'ended_auctions': ended_auctions,
    })


def register(request):
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
        form = SellerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SellerRegisterForm()

    return render(request, 'seller_register.html', {'form': form})









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



@login_required
def logout_view(request):
    logout(request)
    return redirect('/')






User = get_user_model()

@admin_required
def admin_dashboard(request):
    context = {
        'total_users': User.objects.count(),
        'total_auctions': AuctionItem.objects.count(),
        'active_auctions': AuctionItem.objects.filter(is_active=True).count(),
        'total_bids': Bid.objects.count(),
        'auctions': AuctionItem.objects.all()[:5],
    }
    return render(request, 'admin/dashboard.html', context)
