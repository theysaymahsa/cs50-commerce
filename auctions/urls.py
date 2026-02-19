#d
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createListing, name="create"),
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path("listing/<int:listing_id>/watchlist/", views.toggle_watchlist, name="toggle_watchlist"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("listing/<int:listing_id>/bid/", views.place_bid, name="place_bid"),
    path("listing/<int:listing_id>/comment/", views.add_comment, name="add_comment"),
    path("listing/<int:listing_id>/close/", views.close_auction, name="close_auction"),
]
