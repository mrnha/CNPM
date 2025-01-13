from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import *
import json
# Create your views here.
def category(request):
    categories = Category.objects.filter(is_sub=False)
    active_category =request.GET.get('category','')
    products = []
    if active_category:
        products= Product.objects.filter(category__slug=active_category)
    context = {'products':products,'categories':categories,'active_category':active_category}
    return render(request, 'app/category.html', context)

def search(request):
    searched = request.GET.get('searched', '')
    if request.method == "POST":
        searched = request.POST['searched']
        keys = Product.objects.filter(name__contains=searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(Customer=customer, complete=False)
        items = order.orderitem_set.all()

        cartItems = order.get_cart_items     
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    return render(request, 'app/search.html',{"searched":searched,"keys":keys,"items":items,"cartItems":cartItems,"order":order})


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tạo tài khoản thành công')
            return redirect('login')
    context = {'form': form}
    return render(request, 'app/register.html', context)
        
def loginPage(request):  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng')
        except:
            messages.error(request, 'Đã xảy ra lỗi trong quá trình đăng nhập')

    return render(request, 'app/login.html')
def logoutPage(request):
    logout(request)
    return redirect('login')
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(Customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_login = "show"
        User_not_login = "hidden"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_login = "hidden"
        User_not_login = "show"
    categories = Category.objects.filter(is_sub=False)
    products = Product.objects.all()
    context = {'products': products, 'order': order, 'items': items, 'cartItems': cartItems, 'user_login': user_login, 'User_not_login': User_not_login,'categories': categories}
    return render(request, 'app/home.html', context)
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(Customer=customer, complete=False)
        items = order.orderitem_set.all()

        cartItems = order.get_cart_items

        user_login = "show"
        User_not_login = "hidden"
        
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
        user_login = "hidden"
        User_not_login = "show"
    categories = Category.objects.filter(is_sub=False)
        
        
        
    context = {'items': items, 'order': order,'user_login':user_login,'User_not_login':User_not_login,'cartItems':cartItems,'categories':categories}

    return render(request, 'app/cart.html', context)

def new_func(order):
    cartItems = order['get_cart_items']
    return cartItems
def checkout(request):
    context={}
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(Customer=customer, complete=False)
        items = order.orderitem_set.all()

        cartItems = order.get_cart_items

        user_login = "show"
        User_not_login = "hidden"

        
    else:
        items = []
        order = {'order.get_cart_items':0,'order.get_cart_total':0}

        cartItems = order['get_cart_items']
        
        user_login = "hidden"
        User_not_login = "show"
    categories = Category.objects.filter(is_sub=False)
        
        
    context = {'items': items, 'order': order,'user_login':user_login,'User_not_login':User_not_login,'cartItems':cartItems,'categories':categories}

    return render(request, 'app/checkout.html', context)
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action =data['action']
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(Customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity += 1
        orderItem.save()
    elif action == 'remove':
        orderItem.quantity-= 1
        orderItem.save()
        if orderItem.quantity <= 0:
            orderItem.delete()
    
    return JsonResponse('Item was updated', safe=False)
