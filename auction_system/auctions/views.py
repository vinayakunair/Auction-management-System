from django.shortcuts import render, get_object_or_404,redirect
from .models import AuctionItem
from .forms import BidForm,AuctionItemForm
from django.contrib.auth.decorators import login_required
from datetime import timedelta



from django.db.models import Q
from django.utils import timezone
from .models import AuctionItem

# Create your views here.

from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse

@login_required
def auction_detail(request, pk):
    auction = get_object_or_404(AuctionItem, pk=pk)


    if not auction.is_approved:
        return redirect('homepage')


    if auction.has_ended() and auction.winner():
        auction.send_winner_email()

    bids = auction.bids.order_by('-amount')
    form = None

    if request.user.role == 'buyer' and auction.is_live():
        if request.method == 'POST':
            form = BidForm(request.POST)
            if form.is_valid():
                bid = form.save(commit=False)
                bid.auction = auction
                bid.bidder = request.user

                highest = auction.highest_bid()
                current_price = highest.amount if highest else auction.base_price


                if current_price <= 1000:
                    increment = 50
                elif current_price <= 5000:
                    increment = 100
                elif current_price <= 20000:
                    increment = 250
                elif current_price <= 100000:
                    increment = 500
                elif current_price <= 500000:
                    increment = 1000
                else:
                    increment = 5000

                min_bid = current_price + increment

                if bid.amount >= min_bid:
                    bid.save()
                    auction.current_price = bid.amount
                    auction.save()
                    return redirect('auction_detail', pk=auction.pk)
                else:
                    form.add_error('amount', f'Bid must be at least ₹{min_bid} (current: ₹{current_price}, minimum increment: ₹{increment})')
        else:
            form = BidForm()

    return render(request, 'auction_detail.html', {
        'auction': auction,
        'bids': bids,
        'form': form
    })




    


@login_required
def seller_dashboard(request):
    now = timezone.now()

    auctions = AuctionItem.objects.filter(seller=request.user)

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

    return render(request, "seller_dashboard.html", {
        "pending_auctions": pending_auctions,
        "active_auctions": active_auctions,
        "upcoming_auctions": upcoming_auctions,
        "ended_auctions": ended_auctions,
    })






@login_required
def edit_auction(request, pk):
    auction = get_object_or_404(AuctionItem, pk=pk, seller=request.user)

    if auction.is_approved or auction.has_ended():
        return redirect('seller_dashboard')


    
 

    form = AuctionItemForm(
        request.POST or None,
        request.FILES or None,
        instance=auction
    )

    if form.is_valid():
        form.save()
        return redirect('seller_dashboard')

    return render(request, 'auction_form.html', {'form': form})

   





@login_required
def delete_auction(request, pk):
    auction = get_object_or_404(AuctionItem, pk=pk, seller=request.user)

    
    if auction.has_ended() and auction.highest_bid():
        return redirect('seller_dashboard')

    auction.delete()
    return redirect('seller_dashboard')


def category_auctions(request, category):
    now = timezone.now()

    auctions = AuctionItem.objects.filter(
        category=category,
        is_approved=True,
        start_time__lte=now,
        end_time__gt=now
    )

    return render(request, "category_auctions.html", {
        "auctions": auctions,
        "category": category
    })





@login_required
def auction_status_api(request, pk):
    auction = get_object_or_404(AuctionItem, pk=pk)

    if not auction.is_approved:
        return JsonResponse({"error": "Not allowed"}, status=403)

    bids = list(
        auction.bids.order_by('-amount')
        .values('bidder__username', 'amount')
    )

    winner = None
    winning_user = auction.winner()
    if winning_user:
        winner = winning_user.username

    return JsonResponse({
        'status': auction.status(),
        'winner': winner,
        'ended': auction.has_ended(),
        'bids': bids,
    })


@login_required
def create_auction(request):
    if request.user.role != 'seller':
        return redirect('homepage')

    form = AuctionItemForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        auction = form.save(commit=False)
        auction.seller = request.user
        auction.is_approved = False
        auction.current_price = auction.base_price
        auction.save()
        return redirect('seller_dashboard')

    return render(request, 'auction_form.html', {'form': form})



@login_required
def approve_auction(request, pk):
    if request.user.role != 'admin':
        return redirect('homepage')

    auction = get_object_or_404(AuctionItem, pk=pk)

    if not auction.is_approved:
        now = timezone.now()
        auction.is_approved = True
        if auction.start_time is None or auction.start_time > now:
            auction.start_time = now
        auction.save()

    return redirect('admin_dashboard')






@login_required
def seller_auction_detail(request, pk):
    auction = get_object_or_404(
        AuctionItem,
        pk=pk,
        seller=request.user
    )

    bids = auction.bids.order_by('-amount')

    return render(request, "seller_auction_detail.html", {
        "auction": auction,
        "bids": bids,
    })

@login_required
def delete_auction_admin(request, pk):
    if request.user.role != 'admin':
        return redirect('homepage')

    auction = get_object_or_404(AuctionItem, pk=pk)
    auction.delete()
    return redirect('admin_dashboard')

@login_required
def admin_auction_detail(request, pk):
    if request.user.role != 'admin':
        return redirect('homepage')

    auction = get_object_or_404(AuctionItem, pk=pk)
    bids = auction.bids.order_by('-amount')

    return render(request, "admin/auction_detail.html", {
        "auction": auction,
        "bids": bids,
    })
