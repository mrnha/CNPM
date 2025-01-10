from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .models import *
import json


# Create your views here.
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
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

def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'app/home.html', context)
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(Customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        order = {'order.get_cart_items':0,'order.get_cart_total':0}
        
    context = {'items': items, 'order': order}
    return render(request, 'app/cart.html', context)
def checkout(request):
    context={}
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(Customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'order.get_cart_items':0,'order.get_cart_total':0}
        
    context = {'items': items, 'order': order}
    return render(request, 'app/checkout.html', context)
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action  = data['action']
    customer =request.user.customer
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(Customer =customer,complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order =order,product =product)
    if action=='add':
        orderItem.quantity +=1
    elif action =='remove':
        orderItem.quantity -=1
        orderItem.save()
        if orderItem.quantity <=0:
            orderItem.delete()
            return JsonResponse('Item was added', safe=False)
        

