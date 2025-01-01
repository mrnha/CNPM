from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
     path('cart/', views.cart, name='cart'),
      path('checkout/', views.checkout, name='checkout'),
   

]