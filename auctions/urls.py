from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("creating_list",views.creating_list,name="creating_list"),
    path("listing/<int:id>",views.listing,name="listing"),
    path("listing/<int:id>/comment",views.commenting,name="comment"),
    path("listing/<int:id>/watchlist",views.watchlist,name="watchlist"),
    path("watching",views.watching,name="watchingg"),
    path("listing/<int:id>/remove",views.remove_watch,name="remove"),
    path("listing/<int:id>/bid",views.bid,name="bid"),
    path("listing/<int:id>/close",views.close,name="close"),
    path("closeitems",views.closelist,name="closelist"),
    path("category",views.category,name="category")
]

