from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from decimal import Decimal
from django.db.models import Max

from .models import User,auction_list,Comment,Bid,Active


def index(request):
    active_item=auction_list.objects.filter(titlea__active=True)
    return render(request, "auctions/index.html",{
        "auction":active_item
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

@login_required
def creating_list(request):
    if request.method=="POST":
        title=request.POST.get("title")
        description=request.POST.get("description")
        startbid=request.POST.get("starting_bid")
        category=request.POST.get("category")
        url=request.POST.get("url")
        user=request.user
        auction=auction_list.objects.create(title=title,description=description,startbidprice=startbid,category=category,url=url,seller=user)
        Active.objects.create(title=auction)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"auctions/creating_list.html")


def listing(request,id):
    #Get auction_list
    listitem = auction_list.objects.get(pk=id)
    comment = Comment.objects.filter(title=listitem)
    user = request.user
    inwatch = listitem.watch_list.filter(username=user).exists()
    maxbid=Bid.objects.filter(title=listitem).aggregate(Max('bid_price'))['bid_price__max']
    itemactive=Active.objects.get(title=listitem)
    if maxbid is None:
        return render(request,"auctions/listing.html",{
        "listitem":listitem,
        "comment":comment,
        "inwatch":inwatch,
        "nobid":"No bid",
        "user":user,
        "active":itemactive
    })
    else:
        bider=Bid.objects.get(bid_price=maxbid,title=listitem)
        listitem.highestbid=maxbid
        listitem.highestbider=bider.buyer.username
        listitem.save()
        bidmin=maxbid+Decimal("0.01")
        return render(request,"auctions/listing.html",{
        "listitem":listitem,
        "comment":comment,
        "inwatch":inwatch,
        "maxbid":maxbid,
        "bidmin":bidmin,
        "bider":bider,
        "user":user,
        "active":itemactive
    })



def commenting(request,id):
    if request.method == "POST":
        listitem = auction_list.objects.get(pk=id)
        user = request.user
        comment = request.POST.get("comment")
        Comment.objects.create(title=listitem,user=user,comment=comment)
        return HttpResponseRedirect(reverse("listing",args=(listitem.id,)))

def watchlist(request,id):
    if request.method == "POST":
        listitem = auction_list.objects.get(pk=id)
        user = request.user
        Usernow = User.objects.get(username=user)
        Usernow.watchitem.add(listitem)
        #message
        messages.success(request,"Successfully added to the watchlist")
        return HttpResponseRedirect(reverse("listing",args=(listitem.id,)))
        #return render(request,"auctions/listing.html",{
            #"message":"Successfully added to the watchlist",
            #"listitem":listitem
        #})

def remove_watch(request,id):
    if request.method == "POST":
        listitem = auction_list.objects.get(pk=id)
        Usernow = User.objects.get(username=request.user)
        Usernow.watchitem.remove(listitem)
        messages.success(request,"Remove from watchlist")
        return HttpResponseRedirect(reverse("listing",args=(listitem.id,)))

@login_required
def watching(request):
    user = User.objects.get(username=request.user)
    watch = user.watchitem.all()
    active_watchlist = [item for item in watch if item.titlea.filter(active=True).exists()]
    return render(request,"auctions/watch_list.html",{
        "watch":watch,
        "active":active_watchlist
    })

@login_required
def bid(request,id):
    if request.method == "POST":
        listitem = auction_list.objects.get(pk=id)
        bidder = request.user
        bidprice = request.POST.get("bid")
        Bid.objects.create(title=listitem,buyer=bidder,bid_price=bidprice)
        return HttpResponseRedirect(reverse("listing",args=(listitem.id,)))

@login_required
def close(request,id):
    if request.method == "POST":
        listitem=auction_list.objects.get(pk=id)
        activeitem=Active.objects.get(title=listitem)     
        activeitem.active=False
        activeitem.save()
        messages.success(request,"This Bid is close")
        return HttpResponseRedirect(reverse("listing",args=(listitem.id,)))

def closelist(request):
    close_item=auction_list.objects.filter(titlea__active=False)
    return render(request,"auctions/closelist.html",{
        "close":close_item
    })

def category(request):
    return render(request,"auctions/category.html")

def categoryd(request):
    return render(request,"auctions/categoryd.html")