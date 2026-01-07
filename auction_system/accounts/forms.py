from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class RegUser(UserCreationForm):
    role = forms.ChoiceField(
        choices=(('buyer', 'Buyer'), ('seller', 'Seller')),
        widget=forms.RadioSelect
    )

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'role',
            'password1',
            'password2',
        ]

