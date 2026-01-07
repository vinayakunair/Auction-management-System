from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


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

    

    def __str__(self):
        return self.title

    def highest_bid(self):
        return self.bids.order_by('-amount').first()

    def is_live(self):
        now = timezone.now()
        return self.is_active and self.start_time <= now <= self.end_time

    def has_ended(self):
        return timezone.now() > self.end_time

    def status(self):
        highest = self.highest_bid()

        if not self.is_active:
            return "Disabled"

        if timezone.now() < self.start_time:
            return "Upcoming"

        if self.is_live():
            return "Live"

        if self.has_ended():
            if highest and highest.amount >= self.reserve_price:
                return "Ended – Sold"
            return "Ended – Reserve Not Met"
       
    def time_left(self):
        if timezone.now() >= self.end_time:
            return "Ended"

        delta = self.end_time - timezone.now()

        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes = remainder // 60

        if days > 0:
            return f"{days}d {hours}h left"
        if hours > 0:
            return f"{hours}h {minutes}m left"
        return f"{minutes}m left"
    
    def winner(self):
        highest = self.highest_bid()
        if self.has_ended() and highest and highest.amount >= self.reserve_price:
            return highest.bidder
        return None




class Bid(models.Model):
    auction = models.ForeignKey(
        AuctionItem,
        on_delete=models.CASCADE,
        related_name='bids'
    )
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.auction.title + " - " + str(self.amount)





