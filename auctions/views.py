from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, AuctionListing, WatchListItem, Bid, AuctionComment


def categoryPage(request, name):
    listings = AuctionListing.objects.filter(category=name)
    return render(request, "auctions/index.html", {
        "clickCategory": True,
        "category": name,
        "listings": listings
    })

def categories(request):
    listings = AuctionListing.objects.all()
    categories = set()
    for listing in listings:
        categories.add(listing.category)

    return render(request, "auctions/categories.html", {
        "categories": categories
    })

@login_required
def watchlist(request):
    watchlist = request.user.watchlist.all()
    listings = [item.listing for item in watchlist]
    return render(request, "auctions/index.html", {
        "clickWatchlist": True,
        "listings": listings
    })

@login_required
def comment(request, id):
    listing = AuctionListing.objects.get(id=int(id))

    if request.method == "POST":
        comment = AuctionComment(listing=listing, comment=request.POST["comment"], commenter=request.user) 
        comment.save()

        comments = listing.comments.all()
        return HttpResponseRedirect(f"/listing/{id}")

@login_required
def closeAuction(request, id):
    listing = AuctionListing.objects.get(id=int(id))
    listing.closed = True

    listing.winner = listing.bids.order_by('price')[0].bidder
    listing.save()
    return HttpResponseRedirect(f"/listing/{id}")


def bid(request, id):
    listing = AuctionListing.objects.get(id=int(id))
    if request.method == "POST":
        try:
            if float(request.POST["bidPrice"]) >= listing.price:
                listing.price = float(request.POST["bidPrice"])
                listing.save()
                bid = Bid(listing=listing, price=listing.price, bidder=request.user)
                bid.save()
        except:
            pass
    return HttpResponseRedirect(f"/listing/{id}")
    

def listing(request, id):
    listing = AuctionListing.objects.get(id=int(id))
    if request.user == listing.owner:
        owner = True
    else:
        owner = False

    if request.method == "POST":
        watchlisted = request.POST["watchlisted"]
        if watchlisted == "True":
            watchlisted = True
        else:
            watchlisted = False
        if watchlisted:
            item = WatchListItem(user=request.user, listing=listing)
            item.save()
        else:
            WatchListItem.objects.filter(user=request.user, listing=listing).delete()
        return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlisted": watchlisted,
        "owner": owner
        })
    if request.user.is_authenticated:
        comments = listing.comments.all()
        watchlisted = True
        try:
            WatchListItem.objects.get(user=request.user, listing=listing)
            watchlisted = True
        except:
            watchlisted = False
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "watchlisted": watchlisted,
            "owner": owner,
            "comments": comments
        })
    return render(request, "auctions/listing.html", {
        "listing": AuctionListing.objects.get(id=int(id))
    })

def newlisting(request):
    if request.method == "POST":
        name = request.POST["title"]
        price = request.POST["price"]
        description = request.POST["description"]
        category = request.POST["category"]
        imageurl = request.POST["imageurl"]

        listing = AuctionListing(name=name, price=price, extra_detail=description, owner=request.user, category=category, imageurl=imageurl)
        listing.save()
        return render(request, "auctions/new.html", {
            "message": "Listing submitted."
        })

    return render(request, "auctions/new.html")

def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.all()
    })



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
        last_name = request.POST["last_name"]
        first_name = request.POST["first_name"]

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
            user.last_name = last_name
            user.first_name = first_name
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
