from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from decimal import Decimal

from .models import *
import json
def index (request):
    return render(request, 'app/index.html')
# Create your views here.
def detail (request):
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
    
    id = request.GET.get('id', '')
    products = Product.objects.filter(id=id)
    categories = Category.objects.filter(is_sub=False)
        
        
        
    context = {'items': items, 'order': order,'user_login':user_login,'User_not_login':User_not_login,'cartItems':cartItems,'categories':categories,'products':products}

    return render(request, 'app/detail.html', context)


def category(request):
    categories = Category.objects.filter(is_sub=True)
    active_category =request.GET.get('category','')
    products = []
    if active_category:
        products= Product.objects.filter(category__slug=active_category)
        customer = request.user
        order, created = Order.objects.get_or_create(Customer=customer, complete=False)

        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    
    context = {'products':products,'categories':categories,'active_category':active_category, 'order': order, 'items': items, 'cartItems': cartItems}
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
    categories = Category.objects.filter(is_sub=True)
    return render(request, 'app/search.html',{"searched":searched,"keys":keys,"items":items,"cartItems":cartItems,"order":order,"categories":categories})


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
    if request.user.is_authenticated:
        customer = request.user
        order = Order.objects.get(Customer=customer, complete=False)
        items = order.orderitem_set.all()

        if request.method == 'POST':
            try:
                # Tạo shipping address mới
                shipping = ShippingAddress.objects.create(
                    Customer=customer,
                    order=order,
                    full_name=request.POST.get('full_name'),
                    email=request.POST.get('email'),
                    mobile=request.POST.get('mobile'),
                    address=request.POST.get('address'),
                    city=request.POST.get('city'),
                    district=request.POST.get('district'),
                    ward=request.POST.get('ward'),
                    payment_method=request.POST.get('payment_method'),
                    notes=request.POST.get('notes')
                )

                # Cập nhật trạng thái đơn hàng
                order.complete = True
                order.transaction_id = f"ORD-{order.id}"
                order.save()

                # Tạo đơn hàng mới cho khách hàng
                Order.objects.create(Customer=customer, complete=False)

                messages.success(request, 'Đặt hàng thành công! Cảm ơn bạn đã mua hàng.')
                return redirect('home')

            except Exception as e:
                messages.error(request, f'Có lỗi xảy ra: {str(e)}')
                return redirect('checkout')

        context = {
            'items': items,
            'order': order,
        }
        return render(request, 'app/checkout.html', context)
    else:
        messages.warning(request, 'Vui lòng đăng nhập để tiếp tục.')
        return redirect('login')
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
