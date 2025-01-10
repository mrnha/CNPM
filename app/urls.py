from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD

 path('register/', views.register, name="register"),
 path('login/', views.loginPage, name="login"),
 path('', views.home, name="home"),
 path('cart/', views.cart, name="cart"),
 path('checkout/', views.checkout, name="checkout"),
 path('update_item/', views.updateItem, name="update_item"),
 path('logout/', views.logoutPage, name="logout"),   
=======
    path('', views.home, name="home"),
     path('cart/', views.cart, name="cart"),
      path('checkout/', views.checkout, name="checkout"),
       path('update_item/', views.updateItem, name="update_item"), 
   
>>>>>>> parent of d7e0594 (add)

]