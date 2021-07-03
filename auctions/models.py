from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import related
from django.db.models.fields.related import RelatedField

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"

class AuctionListing(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    extra_detail = models.TextField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    category = models.CharField(max_length=25)
    imageurl = models.CharField(max_length=250, default="")
    closed = models.BooleanField(default=False)
    winner = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name}: ${self.price}"

class Bid(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bidder} bid at ${self.price}"

class AuctionComment(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=250)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)

class WatchListItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} {self.listing.id}: {self.listing.name}"