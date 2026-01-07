from django.shortcuts import render, get_object_or_404
from .models import AuctionItem
from .forms import BidForm
from django.contrib.auth.decorators import login_required
# Create your views here.

from django.shortcuts import render

def auction_list(request):
    return render(request, 'auction_list.html')

def auction_detail(request, pk):
    auction = get_object_or_404(AuctionItem, pk=pk)
    bids = auction.bids.order_by('-amount')
    return render(request, 'auction_detail.html', {
        'auction': auction,
        'bids': bids
    })




def auction_detail(request, pk):
    auction = get_object_or_404(AuctionItem, pk=pk)
    bids = auction.bids.order_by('-amount')

    form = None
    if request.user.is_authenticated:
        form = BidForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            bid = form.save(commit=False)
            bid.auction = auction
            bid.bidder = request.user
            bid.save()

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