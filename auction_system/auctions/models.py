from django.db import models
from django.conf import settings
from django.utils import timezone


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
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    is_approved = models.BooleanField(default=False)
    winner_email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def highest_bid(self):
        return self.bids.order_by('-amount').first()

    def is_live(self):
        if not self.is_approved or not self.start_time or not self.end_time:
            return False
        now = timezone.now()
        return self.start_time <= now < self.end_time

    def has_ended(self):
        if not self.end_time:
            return False
        return timezone.now() >= self.end_time

    def status(self):
        now = timezone.now()
        highest = self.highest_bid()

        if not self.is_approved:
            return "Pending Approval"

        if not self.start_time or not self.end_time:
            return "Scheduled"

        if now < self.start_time:
            return "Upcoming"

        if self.start_time <= now < self.end_time:
            return "Live"

        if highest:
            return "Ended – Sold"

        return "Ended – No Bids"

    def time_left(self):
        if not self.end_time:
            return "Not started"

        now = timezone.now()
        if now >= self.end_time:
            return "Ended"

        delta = self.end_time - now
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes = remainder // 60

        if days > 0:
            return f"{days}d {hours}h left"
        if hours > 0:
            return f"{hours}h {minutes}m left"
        return f"{minutes}m left"

    def winner(self):
        if self.has_ended():
            highest = self.highest_bid()
            if highest:
                return highest.bidder
        return None

    def send_winner_email(self):
        from django.core.mail import send_mail
        from django.conf import settings

        if self.winner_email_sent:
            return  

        winner = self.winner()
        if winner and winner.email:
            subject = f'Congratulations! You won the auction for {self.title}'
            message = f'''
Dear {winner.username},

Congratulations! You have won the auction for "{self.title}".

Auction Details:
- Item: {self.title}
- Final Price: ₹{self.current_price}
- Seller: {self.seller.username}

Please contact the seller to arrange payment and delivery.

Thank you for participating in our auction system!

Best regards,
Auction Management Team
'''
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [winner.email],
                    fail_silently=False,
                )
                self.winner_email_sent = True
                self.save()
            except Exception as e:
               
                print(f"Failed to send winner email: {e}")


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
