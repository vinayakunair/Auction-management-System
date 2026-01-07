from django.db import models
from django.conf import settings


CATEGORY_CHOICES = [
    ('electronics', 'Electronics'),
    ('automobile', 'Automobile'),
    ('real_estate', 'Real Estate'),
    ('art', 'Art & Collectibles'),
    ('others', 'Others'),
]


class AuctionItem(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='auction_images/', null=True, blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    reserve_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Bid(models.Model):
    auction = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

