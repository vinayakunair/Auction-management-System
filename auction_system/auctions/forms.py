from django import forms
from .models import Bid,AuctionItem

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']


class AuctionItemForm(forms.ModelForm):
    class Meta:
        model = AuctionItem
        fields = [
            'title',
            'description',
            'category',
            'image',
            'base_price',
            'reserve_price',
            'start_time',
            'end_time',
            'is_active'
        ]