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
            'start_time',
            'end_time',
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

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_time")
        end = cleaned_data.get("end_time")

        if start and end and end <= start:
            raise forms.ValidationError(
                "End time must be after start time."
            )

        return cleaned_data
