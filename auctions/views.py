from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment
from .forms import NewListingForm


def index(request):
    return render(request, "auctions/index.html", {
        "active_listings": Listing.objects.filter(active=True)
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

def new_listing(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            f = Listing(
                title=form_data["title"],
                category = form_data["selected_category"],
                description = form_data["description"],
                startingBid = form_data["starting_bid"],
                imageUrl = form_data["image_url"]
                )
            f.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = NewListingForm()
        return render(request, "auctions/new_listing.html", {
            "form": form
            })
    
def listing_page(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": Comment.objects.filter(commentedListing=listing)
        })
    except:
        return HttpResponseRedirect(reverse("index"))


def place_bid(request, listing_id):
    if request.method == "POST":
        try:
            listing = Listing.objects.get(pk=listing_id)
            if not listing.winning_user:
                placed_bid = int(request.POST["placed_bid"])
                starting_bid = int(listing.startingBid)
                print(placed_bid)
                print(starting_bid)
                if placed_bid < starting_bid:
                    return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))
                else:
                    user_id = request.session.get('_auth_user_id')
                    f = Bid(
                        bidder=User.objects.get(pk=user_id),
                        relatedListing=listing,
                        bid=placed_bid
                        )
                    f.save()

                    listing.winning_user = User.objects.get(pk=user_id)
                    listing.winning_bid = placed_bid
                    listing.save()          

                    return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))   
        except:
            return HttpResponseRedirect(reverse("listing_page", args=(listing.id,))) 

        try:
            listing = Listing.objects.get(pk=listing_id) 
            current_bid = int(listing.winning_bid)
            placed_bid = int(request.POST["placed_bid"])
            if placed_bid <= current_bid:
                print("error")
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "comments": Comment.objects.filter(commentedListing=listing),
                    "message": "Bid is not higher than current bid"
                })
            else:
                user_id = request.session.get('_auth_user_id')
                f = Bid(
                    bidder=User.objects.get(pk=user_id),
                    relatedListing=listing,
                    bid=placed_bid
                    )
                f.save()

                listing.winning_user = User.objects.get(pk=user_id)
                listing.winning_bid = placed_bid
                listing.save()
                

            return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))
        
        except:
            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))
    