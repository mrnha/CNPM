from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect
from .models import *
from django.utils import timezone
import json


from .models import *
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

                # Lưu ID đơn hàng vào session để hiển thị thông báo
                request.session['order_just_completed'] = order.id

                # Tạo đơn hàng mới cho khách hàng
                Order.objects.create(Customer=customer, complete=False)

                messages.success(request, 'Đặt hàng thành công! Cảm ơn bạn đã mua hàng.')
                return redirect('home')

                # Chuyển hướng đến trang xác nhận đơn hàng
                return redirect('order_confirmation', order_id=order.id)

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


@login_required
def account_dashboard(request):
    user = request.user
    profile, created = CustomerProfile.objects.get_or_create(user=user)
    
    # Lấy thông tin giỏ hàng hiện tại
    current_order, created = Order.objects.get_or_create(Customer=user, complete=False)
    cartItems = current_order.get_cart_items
    
    # Lấy lịch sử đơn hàng
    orders = Order.objects.filter(Customer=user, complete=True).order_by('-date_order')
    recent_orders = orders[:5]  # 5 đơn hàng gần nhất
    
    # Thống kê đơn hàng
    total_orders = orders.count()
    total_spent = sum(order.get_cart_total for order in orders)
    
    context = {
        'profile': profile,
        'cartItems': cartItems,
        'current_order': current_order,
        'recent_orders': recent_orders,
        'total_orders': total_orders,
        'total_spent': total_spent,
    }
    return render(request, 'app/account/dashboard.html', context)

@login_required
def account_profile(request):
    user = request.user
    profile, created = CustomerProfile.objects.get_or_create(user=user)
    current_order, created = Order.objects.get_or_create(Customer=user, complete=False)
    cartItems = current_order.get_cart_items

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_profile':
            try:
                # Kiểm tra email
                new_email = request.POST.get('email')
                if new_email != user.email and User.objects.filter(email=new_email).exists():
                    messages.error(request, 'Email này đã được sử dụng.')
                    return redirect('account_profile')
                
                # Cập nhật thông tin cơ bản
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.email = new_email
                user.save()
                
                # Cập nhật thông tin chi tiết
                profile.phone = request.POST.get('phone')
                profile.address = request.POST.get('address')
                profile.city = request.POST.get('city')
                profile.district = request.POST.get('district')
                profile.ward = request.POST.get('ward')
                
                # Xử lý avatar
                if 'avatar' in request.FILES:
                    if profile.avatar:
                        profile.avatar.delete()
                    profile.avatar = request.FILES['avatar']
                
                profile.save()
                messages.success(request, 'Cập nhật thông tin thành công!')
                return redirect('account_profile')
            except Exception as e:
                messages.error(request, f'Lỗi: {str(e)}')
                return redirect('account_profile')

    context = {
        'profile': profile,
        'cartItems': cartItems,
    }
    return render(request, 'app/account/profile.html', context)

@login_required
def account_orders(request):
    user = request.user
    profile, created = CustomerProfile.objects.get_or_create(user=user)
    orders = Order.objects.filter(Customer=user, complete=True).order_by('-date_order')
    current_order, created = Order.objects.get_or_create(Customer=user, complete=False)
    cartItems = current_order.get_cart_items

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_profile':
            try:
                # Kiểm tra email
                new_email = request.POST.get('email')
                if new_email != user.email and User.objects.filter(email=new_email).exists():
                    messages.error(request, 'Email này đã được sử dụng.')
                    return redirect('account_profile')
                
                # Cập nhật thông tin cơ bản
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.email = new_email
                user.save()
                
                # Cập nhật thông tin chi tiết
                profile.phone = request.POST.get('phone')
                profile.address = request.POST.get('address')
                profile.city = request.POST.get('city')
                profile.district = request.POST.get('district')
                profile.ward = request.POST.get('ward')
                
                # Xử lý avatar
                if 'avatar' in request.FILES:
                    if profile.avatar:
                        profile.avatar.delete()
                    profile.avatar = request.FILES['avatar']
                
                profile.save()
                messages.success(request, 'Cập nhật thông tin thành công!')
                return redirect('account_profile')
            except Exception as e:
                messages.error(request, f'Lỗi: {str(e)}')
                return redirect('account_profile')
    
    # Phân trang
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    orders_page = paginator.get_page(page)
    
    context = {
        'profile': profile,
        'orders': orders_page,
        'cartItems': cartItems,
    
    }
    return render(request, 'app/account/orders.html', context)

@login_required
def order_detail(request, order_id):
    user = request.user
    try:
        order = Order.objects.get(id=order_id, Customer=user)
        current_order, created = Order.objects.get_or_create(Customer=user, complete=False)
        cartItems = current_order.get_cart_items
        
        shipping = ShippingAddress.objects.filter(order=order).first()
        items = order.orderitem_set.all()
        
        context = {
            'order': order,
            'shipping': shipping,
            'items': items,
            'cartItems': cartItems,
        }
        return render(request, 'app/account/order_detail.html', context)
    except Order.DoesNotExist:
        messages.error(request, 'Không tìm thấy đơn hàng.')
        return redirect('account_orders')

@login_required
def change_password(request):
    user = request.user
    current_order, created = Order.objects.get_or_create(Customer=user, complete=False)
    cartItems = current_order.get_cart_items
    profile, created = CustomerProfile.objects.get_or_create(user=user)


    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            try:
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Mật khẩu của bạn đã được thay đổi thành công!')
                return redirect('account_dashboard')
            except Exception as e:
                messages.error(request, f'Đã xảy ra lỗi: {str(e)}')
        else:
            messages.error(request, 'Vui lòng kiểm tra lại thông tin nhập vào.')
    else:
        form = PasswordChangeForm(user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_profile':
            try:
                # Kiểm tra email
                new_email = request.POST.get('email')
                if new_email != user.email and User.objects.filter(email=new_email).exists():
                    messages.error(request, 'Email này đã được sử dụng.')
                    return redirect('account_profile')
                
                # Cập nhật thông tin cơ bản
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.email = new_email
                user.save()
                
                # Cập nhật thông tin chi tiết
                profile.phone = request.POST.get('phone')
                profile.address = request.POST.get('address')
                profile.city = request.POST.get('city')
                profile.district = request.POST.get('district')
                profile.ward = request.POST.get('ward')
                
                # Xử lý avatar
                if 'avatar' in request.FILES:
                    if profile.avatar:
                        profile.avatar.delete()
                    profile.avatar = request.FILES['avatar']
                
                profile.save()
                messages.success(request, 'Cập nhật thông tin thành công!')
                return redirect('account_profile')
            except Exception as e:
                messages.error(request, f'Lỗi: {str(e)}')
                return redirect('account_profile')

    context = {
        'profile': profile,
        'form': form,
        'cartItems': cartItems,
    }
    return render(request, 'app/account/change_password.html', context)

@login_required
@require_POST
@csrf_protect
def update_avatar(request):
    try:
        if request.FILES.get('avatar'):
            profile = request.user.customerprofile
            # Xóa avatar cũ nếu có
            if profile.avatar:
                profile.avatar.delete()
            
            profile.avatar = request.FILES['avatar']
            profile.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Avatar đã được cập nhật thành công',
                'avatar_url': profile.avatar.url
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)
def get_context_data(request):
    context = {}
    if request.user.is_authenticated:
        try:
            customer = request.user.customerprofile
            pending_orders = Order.objects.filter(Customer=customer, complete=False).count()
            context['pending_orders_count'] = pending_orders
            
            # Thêm cartItems vào context
            order, created = Order.objects.get_or_create(Customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = sum([item.quantity for item in items])
            context['cartItems'] = cartItems
            
        except Exception as e:
            print(f"Error in get_context_data: {e}")
            context['pending_orders_count'] = 0
            context['cartItems'] = 0
            
    return context

def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id, is_active=True)
        # Tăng lượt xem
        blog.views += 1
        blog.save()
        
        # Lấy các bài viết liên quan
        related_blogs = Blog.objects.filter(
            category=blog.category,
            is_active=True
        ).exclude(id=blog_id)[:3]
        
        # Lấy comments
        comments = blog.comments.filter(is_active=True)
        
        # Xử lý comment mới
        if request.method == 'POST' and request.user.is_authenticated:
            content = request.POST.get('content')
            if content:
                BlogComment.objects.create(
                    blog=blog,
                    user=request.user,
                    content=content
                )
                messages.success(request, 'Bình luận của bạn đã được gửi thành công!')
                return redirect('blog_detail', blog_id=blog_id)
        
        # Lấy thông tin giỏ hàng
        if request.user.is_authenticated:
            customer = request.user
            order, created = Order.objects.get_or_create(Customer=customer, complete=False)
            cartItems = order.get_cart_items
        else:
            order = {'get_cart_total': 0, 'get_cart_items': 0}
            cartItems = order['get_cart_items']
        
        context = {
            'blog': blog,
            'related_blogs': related_blogs,
            'comments': comments,
            'cartItems': cartItems
        }
        return render(request, 'app/blog_detail.html', context)
    
    except Blog.DoesNotExist:
        messages.error(request, 'Không tìm thấy bài viết này!')
        return redirect('home')

def promotions(request):
    # Lấy tất cả khuyến mãi còn hiệu lực
    active_promotions = Promotion.objects.filter(
        is_active=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).order_by('-start_date')

    # Lấy khuyến mãi nổi bật (có ảnh banner)
    featured_promotions = active_promotions.exclude(banner_image='')[:5]

    context = {
        'promotions': active_promotions,
        'featured_promotions': featured_promotions
    }
    return render(request, 'app/promotions.html', context)

def format_price(value):
    """Helper function để format giá tiền"""
    try:
        return f"{int(value):,}₫"
    except (ValueError, TypeError):
        return "0₫"

@require_http_methods(["POST"])
def apply_promotion(request):
    try:
        data = json.loads(request.body)
        code = data.get('code')
        order_total = float(data.get('order_total', 0))
        
        try:
            promotion = Promotion.objects.get(
                code=code,
                is_active=True,
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now()
            )
            
            # Kiểm tra giá trị đơn hàng tối thiểu
            if order_total < promotion.min_order_value:
                return JsonResponse({
                    'valid': False,
                    'message': f'Đơn hàng tối thiểu phải từ {format_price(promotion.min_order_value)}'
                })
            
            # Tính số tiền giảm
            if promotion.discount_type == 'PERCENT':
                discount_amount = (order_total * promotion.discount_percent) / 100
                if promotion.max_discount_amount:
                    discount_amount = min(discount_amount, promotion.max_discount_amount)
                discount_display = f"{promotion.discount_percent:.1f}%"
            else:
                discount_amount = promotion.discount_amount
                discount_display = format_price(promotion.discount_amount)
            
            final_total = order_total - discount_amount
            
            return JsonResponse({
                'valid': True,
                'discount_display': discount_display,
                'discount_amount': discount_amount,
                'discount_amount_display': format_price(discount_amount),
                'final_total_display': format_price(final_total)
            })
            
        except Promotion.DoesNotExist:
            return JsonResponse({
                'valid': False,
                'message': 'Mã khuyến mãi không hợp lệ hoặc đã hết hạn'
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'valid': False,
            'message': 'Dữ liệu không hợp lệ'
        })
    except Exception as e:
        return JsonResponse({
            'valid': False,
            'message': 'Có lỗi xảy ra, vui lòng thử lại'
        })


    