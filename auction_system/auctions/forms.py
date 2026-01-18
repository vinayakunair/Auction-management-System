from django import forms
from .models import Bid, AuctionItem
from django import forms
from django.utils import timezone
from .models import Bid, AuctionItem



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

        widgets = {
            'start_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'min': timezone.now().strftime('%Y-%m-%dT%H:%M')
                }
            ),
            'end_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'min': timezone.now().strftime('%Y-%m-%dT%H:%M')
                }
            ),
        }
