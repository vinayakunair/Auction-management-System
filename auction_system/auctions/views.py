from django.shortcuts import render, get_object_or_404,redirect
from .models import AuctionItem
from .forms import BidForm,AuctionItemForm
from django.contrib.auth.decorators import login_required
# Create your views here.

from django.shortcuts import render

def auction_list(request):
    return render(request, 'auction_list.html')

@login_required
def auction_detail(request, pk):
    auction = get_object_or_404(AuctionItem, pk=pk)
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
                min_bid = highest.amount if highest else auction.base_price

                if bid.amount > min_bid:
                    bid.save()
                    return redirect('auction_detail', pk=auction.pk)
                else:
                    form.add_error('amount', 'Bid must be higher than current bid')
        else:
            form = BidForm()

    return render(request, 'auction_detail.html', {
        'auction': auction,
        'bids': bids,
        'form': form
    })



@login_required
def seller_dashboard(request):
    auctions = AuctionItem.objects.filter(seller=request.user)
    return render(request, 'seller_dashboard.html', {'auctions': auctions})


@login_required
def create_auction(request):
    form = AuctionItemForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        auction = form.save(commit=False)
        auction.seller = request.user
        auction.save()
        return redirect('seller_dashboard')
    return render(request, 'auction_form.html', {'form': form})


@login_required
def edit_auction(request, pk):
    auction = get_object_or_404(AuctionItem, pk=pk, seller=request.user)
    form = AuctionItemForm(request.POST or None, request.FILES or None, instance=auction)
    if form.is_valid():
        form.save()
        return redirect('seller_dashboard')
    return render(request, 'auction_form.html', {'form': form})


@login_required
def delete_auction(request, pk):
    auction = get_object_or_404(AuctionItem, pk=pk, seller=request.user)
    auction.delete()
    return redirect('seller_dashboard')