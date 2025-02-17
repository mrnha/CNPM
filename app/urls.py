from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

 path('', views.home, name="home"),
 path('detail/', views.detail, name="detail"),
 path('register/', views.register, name="register"),
 path('login/', views.loginPage, name="login"),
 path('search/', views.search, name="search"),
 path('cart/', views.cart, name="cart"),
 path('checkout/', views.checkout, name="checkout"),
 path('update_item/', views.updateItem, name="update_item"),
 path('logout/', views.logoutPage, name="logout"),   
 path('category/', views.category, name="category"),
 path('account/', views.account_dashboard, name='account_dashboard'),
 path('account/orders/', views.account_orders, name='account_orders'),
 path('account/profile/', views.account_profile, name='account_profile'),
 path('account/orders/<int:order_id>/', views.order_detail, name='order_detail'),
 path('account/change-password/', views.change_password, name='change_password'),
 path('account/update-avatar/', views.update_avatar, name='update_avatar'),
 path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
 path('promotions/', views.promotions, name='promotions'),
 path('apply-promotion/', views.apply_promotion, name='apply_promotion'),
 path('about/', views.about, name='about'),
]