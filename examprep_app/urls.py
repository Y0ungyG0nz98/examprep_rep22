from django.urls import path
from . import views
urlpatterns = [
    path("", views.index),
    path("register", views.registerUser),
    path("home", views.home),
    path("logout", views.logout),
    path("login", views.login),
    path("trip/add", views.tripAdd), #("wishes/add", views.wishAdd),
    path("createtrip", views.create), #("createTrip", views.create),
    path('addtoFav/<int:itemId>', views.addToFav),
    path("removefromFav/<int:itemId>", views.removefromFav),
    path("delete/<int:itemId>", views.deleteItem),
    path("items/<int:itemId>", views.destinations) #("items/<int:itemId>"), views.showItem
]