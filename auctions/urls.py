from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_listing, name="new_listing"),
    path("<int:listing_id>", views.listing_page, name="listing_page"),
    path("place_bid/<int:listing_id>", views.place_bid, name="place_bid")
]
