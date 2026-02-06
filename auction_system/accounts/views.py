from django.shortcuts import render,redirect
from .forms import RegUser,SellerRegisterForm

from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from .models import CustomUser
from django.utils import timezone
from django.db import models
from django.db.models import F

from .decorators import admin_required
from auctions.models import AuctionItem, Bid
from django.contrib.auth import get_user_model


# Create your views here.

from django.shortcuts import get_object_or_404







from django.utils import timezone
from auctions.models import AuctionItem

def homepage(request):
    now = timezone.now()

    upcoming_auctions = AuctionItem.objects.filter(
        is_approved=True,
        start_time__gt=now
    )

    active_auctions = AuctionItem.objects.filter(
        is_approved=True,
        start_time__lte=now,
        end_time__gt=now
    )

    ended_auctions = AuctionItem.objects.filter(
        end_time__lte=now
    )

    return render(request, "homepage.html", {
        "upcoming_auctions": upcoming_auctions,
        "active_auctions": active_auctions,
        "ended_auctions": ended_auctions,
    })




def register(request):
    if request.method == 'POST':
        form = RegUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
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
            if user.is_blocked:
                return render(request, 'login.html', {'error': 'Your account has been blocked. Please contact admin.'})
            login(request, user)
            return redirect('homepage')

    return render(request, 'login.html')



@login_required
def logout_view(request):
    logout(request)
    return redirect('login')






User = get_user_model()

@admin_required
def admin_dashboard(request):
    now = timezone.now()

    active_auctions_qs = AuctionItem.objects.filter(
        is_approved=True,
        start_time__lte=now,
        end_time__gt=now
    )

    upcoming_auctions_qs = AuctionItem.objects.filter(
        is_approved=True,
        start_time__gt=now
    )

    ended_auctions_qs = AuctionItem.objects.filter(
        end_time__lte=now
    )

    context = {
        'total_users': User.objects.count(),
        'total_sellers': User.objects.filter(role='seller').count(),
        'total_buyers': User.objects.filter(role='buyer').count(),
        'total_auctions': AuctionItem.objects.count(),

        'active_auctions': active_auctions_qs.count(),
        'upcoming_auctions': upcoming_auctions_qs.count(),
        'ended_auctions': ended_auctions_qs.count(),

        'active_auctions_list': active_auctions_qs[:5],
        'upcoming_auctions_list': upcoming_auctions_qs[:5],
        'ended_auctions_list': ended_auctions_qs[:5],

        'active_auctions_full': active_auctions_qs,
        'upcoming_auctions_full': upcoming_auctions_qs,
        'ended_auctions_full': ended_auctions_qs,

        'total_bids': Bid.objects.count(),
        'auctions': AuctionItem.objects.order_by('-created_at')[:5],
        'users': User.objects.exclude(role='admin').order_by('-date_joined')[:10],
    }

    return render(request, 'admin/dashboard.html', context)



@admin_required
def approve_auction(request, auction_id):
    if request.method != "POST":
        return redirect('admin_dashboard')

    auction = get_object_or_404(AuctionItem, id=auction_id)

    if auction.is_approved or auction.has_ended():
        return redirect('admin_dashboard')

    auction.is_approved = True
    auction.save()

    return redirect('admin_dashboard')




@admin_required
def disable_auction(request, auction_id):
    if request.method != "POST":
        return redirect('admin_dashboard')

    auction = get_object_or_404(AuctionItem, id=auction_id)

    if auction.has_ended():
        return redirect('admin_dashboard')

    auction.is_approved = False
    auction.save()

    return redirect('admin_dashboard')


@admin_required
def block_user(request, user_id):
    if request.method != "POST":
        return redirect('admin_dashboard')

    user = get_object_or_404(User, id=user_id)

    if user.role == 'admin':
       
        return redirect('admin_dashboard')

    user.is_blocked = True
    user.save()

    return redirect('admin_dashboard')


@admin_required
def unblock_user(request, user_id):
    if request.method != "POST":
        return redirect('admin_dashboard')

    user = get_object_or_404(User, id=user_id)

    user.is_blocked = False
    user.save()

    return redirect('admin_dashboard')


@admin_required
def admin_users_list(request):
    users = User.objects.exclude(role='admin').order_by('-date_joined')
    return render(request, "admin/users_list.html", {
        "users": users,
    })

@admin_required
def admin_user_auctions(request, user_id):
    user = get_object_or_404(User, id=user_id)
    now = timezone.now()

    if user.role == 'seller':
        auctions = AuctionItem.objects.filter(seller=user)

        pending_auctions = auctions.filter(is_approved=False)

        active_auctions = auctions.filter(
            is_approved=True,
            start_time__lte=now,
            end_time__gt=now
        )

        upcoming_auctions = auctions.filter(
            is_approved=True,
            start_time__gt=now
        )

        ended_auctions = auctions.filter(
            is_approved=True,
            end_time__lte=now
        )

        return render(request, "admin/user_auctions.html", {
            "user": user,
            "pending_auctions": pending_auctions,
            "active_auctions": active_auctions,
            "upcoming_auctions": upcoming_auctions,
            "ended_auctions": ended_auctions,
        })
    else:
        
        bids = Bid.objects.filter(bidder=user).select_related('auction')

        active_bids = bids.filter(
            auction__is_approved=True,
            auction__start_time__lte=now,
            auction__end_time__gt=now
        )

        ended_bids = bids.filter(
            auction__end_time__lte=now
        )

        return render(request, "admin/user_auctions.html", {
            "user": user,
            "active_auctions": active_bids,
            "ended_auctions": ended_bids,
        })

@login_required
def buyer_dashboard(request):
    if request.user.role != 'buyer':
        return redirect('homepage')

    now = timezone.now()

    ended_auctions_with_bids = AuctionItem.objects.filter(
        bids__bidder=request.user,
        end_time__lte=now
    ).distinct()

    
    won_auctions = []
    for auction in ended_auctions_with_bids:
        if auction.winner() == request.user:
            won_auctions.append(auction)

    return render(request, "buyer_dashboard.html", {
        "won_auctions": won_auctions,
    })

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            
            import random
            otp = str(random.randint(100000, 999999))

        
            request.session['reset_otp'] = otp
            request.session['reset_email'] = email

            
            subject = 'Password Reset OTP'
            message = f'Your OTP for password reset is: {otp}\n\nThis OTP will expire in 10 minutes.'
            from_email = 'vinayakunair@gmail.com' 
            recipient_list = [email]

            try:
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, 'OTP sent to your email. Please check your email.')
            except Exception as e:
                messages.error(request, 'Failed to send email. Please try again later.')
                return render(request, 'password_reset_request.html')
            return redirect('password_reset_verify')
        except CustomUser.DoesNotExist:
            messages.error(request, 'No account found with this email address.')

    return render(request, 'password_reset_request.html')

def password_reset_verify(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if otp == request.session.get('reset_otp'):
            if new_password == confirm_password:
                email = request.session.get('reset_email')
                try:
                    user = CustomUser.objects.get(email=email)
                    user.set_password(new_password)
                    user.save()

                   
                    del request.session['reset_otp']
                    del request.session['reset_email']

                    messages.success(request, 'Password reset successfully. Please login with your new password.')
                    return redirect('loginpage')
                except CustomUser.DoesNotExist:
                    messages.error(request, 'User not found.')
            else:
                messages.error(request, 'Passwords do not match.')
        else:
            messages.error(request, 'Invalid OTP.')

    return render(request, 'password_reset_verify.html')

@admin_required
def admin_seller_auctions(request, seller_id):
    seller = get_object_or_404(User, id=seller_id, role='seller')
    now = timezone.now()

    auctions = AuctionItem.objects.filter(seller=seller)

    pending_auctions = auctions.filter(is_approved=False)

    active_auctions = auctions.filter(
        is_approved=True,
        start_time__lte=now,
        end_time__gt=now
    )

    upcoming_auctions = auctions.filter(
        is_approved=True,
        start_time__gt=now
    )

    ended_auctions = auctions.filter(
        is_approved=True,
        end_time__lte=now
    )

    return render(request, "admin/seller_auctions.html", {
        "seller": seller,
        "pending_auctions": pending_auctions,
        "active_auctions": active_auctions,
        "upcoming_auctions": upcoming_auctions,
        "ended_auctions": ended_auctions,
    })

