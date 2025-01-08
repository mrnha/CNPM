from urllib import request
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import *
import json
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(Customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    context = {'products': products, 'order': order, 'items': items,'cartItems':cartItems}
    return render(request, 'app/home.html', context)
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(Customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        order = {'order.get_cart_items':0,'order.get_cart_total':0}
        cartItems = order['get_cart_items']
        
        
    context = {'items': items, 'order': order,'cartItems':cartItems}
    return render(request, 'app/cart.html', context)
def checkout(request):
    context={}
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(Customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'order.get_cart_items':0,'order.get_cart_total':0}
        cartItems = order['get_cart_items']
        
    context = {'items': items, 'order': order,'cartItems':cartItems}
    return render(request, 'app/checkout.html', context)
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action =data['action']
    customer = request.user.customer
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
