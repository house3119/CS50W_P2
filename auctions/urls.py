from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_listing, name="new_listing"),
    path("<int:listing_id>", views.listing_page, name="listing_page"),
    path("place_bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("open/<int:listing_id>", views.open, name="open"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.category_page, name="category_page"),
    path("categories/<str:category_name>", views.category, name="category")
]
