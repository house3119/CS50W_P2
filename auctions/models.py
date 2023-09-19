from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    imageUrl = models.URLField(max_length=100, blank=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usersListings", default=1)
    startingBid = models.IntegerField()
    category_choices = (
        ("EL", "Electronics"),
        ("FA", "Fashion"),
        ("FU", "Furniture"),
        ("TO", "Toys"),
        ("OT", "Other"),
    )
    category = models.CharField(max_length=2, choices=category_choices, default="OT")
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    watchers = models.ManyToManyField(User, blank=True, related_name="watching")
    winning_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="usersWinningBids")
    winning_bid = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usersBids", default=1)
    relatedListing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingsBids")
    bid = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"€{self.bid} on {self.relatedListing.title}, bidder: {self.bidder}"


class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usersComments")
    commentedListing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingsComments")
    comment = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.commentedListing.title} by {self.commenter}"