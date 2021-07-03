from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("listing/<int:id>/close", views.closeAuction, name="close"),
    path("listing/<int:id>/comment", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:name>", views.categoryPage, name="categoryPage")
]
