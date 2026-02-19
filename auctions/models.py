#D
from django.db import models
from django.contrib.auth.models import AbstractUser

class User (AbstractUser):
    pass

class Category(models.Model):
    name=models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Listing(models.Model):
    title=models.CharField(max_length=64)
    description=models.TextField()
    image_url=models.URLField(blank=True)
    price=models.FloatField()
    isActive=models.BooleanField(default=True)

    title=models.CharField(max_length=64)
    description=models.TextField()
    price=models.FloatField()
    image_url=models.URLField(blank=True)
    category=models.CharField(max_length=64)
    owner=models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

    is_active=models.BooleanField(default=True)
    winner=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="won_listings")

    owner==models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="listings_owned")

    category=models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="listings")

    watchlist=models.ManyToManyField(User, blank=True, related_name="watchlist_items")

    def __str__(self):
        return self.title

class Bid(models.Model):
    listing=models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount=models.FloatField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"${self.amount} by {self.user.username}" #

class Comment(models.Model):
    listing=models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"
