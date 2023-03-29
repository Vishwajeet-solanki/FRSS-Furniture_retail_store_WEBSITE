from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [    
path('', views.index, name="ShopHome"),
path("about/", views.about, name="AboutUs"),
path("contact/", views.contact, name="ContactUs"),
path("search/", views.search, name="Search"),
path("signup/", views.signup, name="Search"),
path("login/", views.log_in, name="Search"),
path("products/<int:id>", views.productView, name="ProductView"),
path("checkout/", views.checkout, name="Checkout"),
]