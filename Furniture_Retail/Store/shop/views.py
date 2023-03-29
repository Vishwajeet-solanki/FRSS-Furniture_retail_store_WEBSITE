from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import *
import math
import logging
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django import forms
from datetime import date
from django.contrib.auth.models import User

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + math.ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds':allProds}
    return render(request,"index.html", params)

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'contact.html')

def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("This is not a customer id")
            else:
                return redirect("/index")
        else:
            alert = True
            return render(request, "login.html", {'alert': alert})
    return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match")

        user = User.objects.create_user(
            username=username, email=email, password=password, first_name=first_name, last_name=last_name)

        customer = Customer.objects.create(user=user, first_name=first_name, last_name=last_name, email=email,
                                         phone=phone)
        user.save()
        customer.save()

        alert = True
        return render(request, "signup.html", {'alert': alert})
    return render(request, "signup.html")

def search(request):
    return render(request, 'search.html')

def productView(request, id):
    # Fetch the product using the id
    product = Product.objects.filter(id=id)


    return render(request, 'prodView.html', {'product':product[0]})

def checkout(request):
    return render(request, 'checkout.html')