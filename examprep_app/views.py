from django.shortcuts import render, redirect
from .models import User, Item
from django.contrib import messages
import bcrypt
from django.db.models import Q


def index(request):
    return render(request, 'index.html')


def registerUser(request):
    print(request.POST)
    validationErrors = User.objects.registrationValidator(request.POST)
    print(validationErrors)
    if len(validationErrors)> 0:
        for key, value in validationErrors.items():
            messages.error(request, value)
        return redirect("/")
    hashedPW = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
    newuser = User.objects.create(firstName = request.POST['fname'], lastName = request.POST['lname'], email = request.POST['email'], password = hashedPW)
    request.session['loggedinId'] = newuser.id
    return redirect("/home")

def home(request):
    if 'loggedinId' not in request.session:
        return redirect("/")
    loggedinuser = User.objects.get(id = request.session['loggedinId'])
    context = {
        'loggedinUser': loggedinuser,
        'mywishes': Item.objects.filter(Q(uploader = loggedinuser) | Q(favoritor = loggedinuser)),
        'notMywishes': Item.objects.exclude(Q(uploader = loggedinuser) | Q(favoritor = loggedinuser))
    }
    
    return render(request, "home.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")

def login(request):
    print(request.POST)
    validation_errors = User.objects.loginValidator(request.POST)
    print(validation_errors)
    if len(validation_errors)>0:
        for key,value in validation_errors.items():
            messages.error(request, value) 
        return redirect("/")
    
    user = User.objects.get(email = request.POST['email'])
    request.session['loggedinId'] = user.id
    return redirect("/home")

def tripAdd(request):
    return render(request, "addtrip.html")      #"addtrip.html"

def create(request):
    print(request.POST)
    validationErrors = Item.objects.validateItem(request.POST)
    if len(validationErrors)>0:
        for key,value in validationErrors.items():
            messages.error(request, value)
        return redirect('trip/add')     #''
    loggedinuser = User.objects.get(id = request.session['loggedinId'])
    newWish = Item.objects.create(name = request.POST['itemName'], uploader = loggedinuser)     #newWish
    return redirect("/home")

def addToFav(request, itemId):
    loggedinuser = User.objects.get(id = request.session['loggedinId'])
    item = Item.objects.get(id = itemId)
    item.favoritor.add(loggedinuser)
    return redirect("/home")

def removefromFav(request, itemId):
    loggedinuser = User.objects.get(id = request.session['loggedinId'])
    item = Item.objects.get(id = itemId)
    item.favoritor.remove(loggedinuser)
    return redirect("/home")

def deleteItem(request, itemId):
    item = Item.objects.get(id = itemId)
    item.delete()
    return redirect("/home")

def destinations(request, itemId):      #showItem
    context = {
        'itemToShow': Item.objects.get(id = itemId)
    }
    return render(request, "destinations.html", context)

