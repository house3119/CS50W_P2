from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, User
from .forms import NewListingForm


def clearError(request):
    try:
        request.session.pop("errormessage")
        return
    except:
        return


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
                imageUrl = form_data["image_url"],
                poster = User.objects.get(pk=request.session.get('_auth_user_id'))
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
        error = request.session.get("errormessage")
    except:
        pass
    clearError(request)
    
    try:
        listing = Listing.objects.get(pk=listing_id)
        is_following = False
        if request.session.get('_auth_user_id'):               
            user = User.objects.get(pk=request.session.get('_auth_user_id'))
            if user in listing.watchers.all():
                is_following = True
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": Comment.objects.filter(commentedListing=listing),
            "is_following":is_following,
            "error": error
        })
    except:
        return HttpResponseRedirect(reverse("index"))


def place_bid(request, listing_id):
    clearError(request)
    if request.method == "POST":
        try:
            listing = Listing.objects.get(pk=listing_id)
            if not listing.winning_user:
                placed_bid = int(request.POST["placed_bid"])
                starting_bid = int(listing.startingBid)
                if placed_bid < starting_bid:
                    request.session["errormessage"] = "Bid is not higher or equal to starting bid."
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
                request.session["errormessage"] = "Bid is not higher than current leading bid."
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
            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))


def add_comment(request, listing_id):
    if request.method == "POST":
        try:
            listing = Listing.objects.get(pk=listing_id)
            new_comment = request.POST["placed_comment"]
            if new_comment == "":
                return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))
            else:
                user_id = request.session.get('_auth_user_id')
                f = Comment(
                    commenter=User.objects.get(pk=user_id),
                    commentedListing=listing,
                    comment=new_comment
                )
                f.save()
                return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))
        except:
            return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))
    else:
        return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))
    

def add_to_watchlist(request, listing_id):
    if request.method == "POST":
        try:
            listing = Listing.objects.get(pk=listing_id)
            user_id = request.session.get('_auth_user_id')
            listing.watchers.add(User.objects.get(id=user_id))
            listing.save()
            return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))
        except:
            return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))
        

def remove_from_watchlist(request, listing_id):
    if request.method == "POST":
        try:
            listing = Listing.objects.get(pk=listing_id)
            user_id = request.session.get('_auth_user_id')
            listing.watchers.remove(User.objects.get(id=user_id))
            listing.save()
            return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))
        except:
            return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))
    else:
        return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))


def close(request, listing_id):
    if request.method == "POST":
        try:
            listing = Listing.objects.get(pk=listing_id)
            listing.active = False
            listing.save()
            return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))
        except:
            return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))
    else:
        return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))


def open(request, listing_id):
    if request.method == "POST":
        try:
            listing = Listing.objects.get(pk=listing_id)
            listing.active = True
            listing.save()
            return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))
        except:
            return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))
    else:
        return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))


def watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    else:
        listings = Listing.objects.all()
        return render(request, "auctions/watchlist.html", {
            "listings": listings
        })
    

def category_page(request):
    categories = Listing.category_choices
    holder = []
    for i in categories:
        holder.append(i[1])
    return render(request, "auctions/category_page.html", {
        "categories": holder
    })
    

def category(request, category_name):
    try:
        listings = Listing.objects.filter(category=category_name[:2].upper(), active=True)
        return render(request, "auctions/category.html", {
            "category": category_name,
            "listings": listings
        })
    except:
        return HttpResponseRedirect(reverse("index"))