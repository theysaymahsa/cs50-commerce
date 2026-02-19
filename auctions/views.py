from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Listing
from django.shortcuts import render, get_object_or_404
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import User, Category, Listing
from .models import Bid
from .models import Comment





def index(request):
    category_id=request.GET.get("category")

    if category_id:
        activeListings=Listing.objects.filter(
            isActive=True,
            category__id=category_id
        )
    else:
        activeListings=Listing.objects.filter(isActive=True)

    allCategories=Category.objects.all()
    return render(request, "auctions/index.html",{
            "listings":activeListings,
            "categories":allCategories
        })

def createListing(request):
     if request.method == "GET":
         allCategories=Category.objects.all()
         return render(request, "auctions/create.html", {
             "categories": allCategories
         })
     else:
         title=request.POST["title"]
         description=request.POST["description"]
         image_url=request.POST["imageurl"]
         price=request.POST["price"]
         category_id=request.POST["category"]

         currentUser=request.user

         category_id=request.POST["category"]
         categoryData=Category.objects.get(id=category_id)

         newListing=Listing(
             title=title,
             description=description,
             image_url=image_url,
             price=price,
             category=categoryData,
             owner=currentUser,
         )
         newListing.save()
         return HttpResponseRedirect(reverse(index))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request, listing_id):
    listing=get_object_or_404(Listing,pk=listing_id)
    return render(request, "auctions/listing.html",{
        "listing":listing
    })

def toggle_watchlist(request, listing_id):
    listing=get_object_or_404(Listing, id=listing_id)
    user=request.user

    if listing.watchlist.filter(id=user.id).exists():
        listing.watchlist.remove(user)
    else:
        listing.watchlist.add(user)
    return redirect("listing", listing_id=listing_id)

def watchlist(request):
    if not request.user.is_authenticated:
        return redirect("login")

    listings=request.user.watchlist_items.all()
    return render(request, "auctions/watchlist.html", {
        "listings":listings
    })

def place_bid(request, listing_id):
    listing=get_object_or_404(Listing, id=listing_id)
    user=request.user

    if request.method=="POST":
        bid_amount=float(request.POST["bid_amount"])
        current_highest=listing.bids.order_by("-amount").first()
        highest_amount=current_highest.amount if current_highest else listing.price

        if bid_amount > highest_amount:
            Bid.objects.create(listing=listing, user=user, amount=bid_amount)
            listing.orice=bid_amount
            listing.save()
            messages.success(request, "Bid placed successefully!")
        else:
            messages.error(request, f"Your bid must be higher than {highest_amount}.")
    return redirect("listing", listing_id=listing.id)  #a

def add_comment(request, listing_id):
    listing=get_object_or_404(Listing, id=listing_id)

    if request.method=="POST":
        content=request.POST["comment"]
        Comment.objects.create(listing=listing, user=request.user, content=content)
    return redirect("listing", listing_id=listing.id)

def close_auction(request, listing_id):
    listing=get_object_or_404(Listing, id=listing_id)

    if request.user != listing.owner:
        messages.error(request, "You are not allowed to close this auction.")
        return redirect("listing", listing_id=listing.id)
    highest_bid=listing.bids.order_by("-amount").first()

    if highest_bid:
        listing.winner=highest_bid.user

    listing.is_active=False
    listing.save()
    messages.success(request, "Auction closed successfully!")
    return redirect("listing", listing_id=listing.id)


