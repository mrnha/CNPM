from django.db import models # type: ignore
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

# Create your models here.

class Category (models.Model):
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE,related_name='sub_categories',null=True,blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name
    

class CreateUserForm(UserCreationForm):
 class Meta:
        model =User
        fields =['username','email','first_name','last_name','password1','password2']

    
class Product(models.Model):
    category = models.ManyToManyField(Category,related_name='products')
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    detail = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    Customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null = True)

    def __str__(self):
        return str(self.id)
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems ])
        return total 
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems ])
        return total 
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total 

class ShippingAddress(models.Model):
    Customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, verbose_name="Họ và tên")
    email = models.EmailField(max_length=200, null=True, verbose_name="Email")
    address = models.CharField(max_length=200, null=True, verbose_name="Địa chỉ")
    city = models.CharField(max_length=200, null=True, verbose_name="Thành phố")
    district = models.CharField(max_length=200, null=True, verbose_name="Quận/Huyện")
    ward = models.CharField(max_length=200, null=True, verbose_name="Phường/Xã")
    mobile = models.CharField(max_length=15, null=True, verbose_name="Số điện thoại")
    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('COD', 'Thanh toán khi nhận hàng'),
            ('BANK', 'Chuyển khoản ngân hàng'),
            ('MOMO', 'Ví MoMo'),
            ('VNPAY', 'VNPay'),
        ],
        default='COD',
        verbose_name="Phương thức thanh toán"
    )
    notes = models.TextField(null=True, blank=True, verbose_name="Ghi chú")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Đơn hàng của {self.full_name}"

    class Meta:
        verbose_name = "Địa chỉ giao hàng"
        verbose_name_plural = "Địa chỉ giao hàng"
    

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name="Số điện thoại")
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name="Địa chỉ")
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name="Thành phố")
    district = models.CharField(max_length=100, null=True, blank=True, verbose_name="Quận/Huyện")
    ward = models.CharField(max_length=100, null=True, blank=True, verbose_name="Phường/Xã")

    def __str__(self):
        return f"Hồ sơ của {self.user.username}"

    class Meta:
        verbose_name = "Hồ sơ khách hàng"
        verbose_name_plural = "Hồ sơ khách hàng"
    

class BlogCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tên danh mục")
    slug = models.SlugField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Danh mục bài viết"
        verbose_name_plural = "Danh mục bài viết"

class Blog(models.Model):
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='blogs')
    title = models.CharField(max_length=300, verbose_name="Tiêu đề")
    slug = models.SlugField(max_length=300, unique=True)
    content = models.TextField(verbose_name="Nội dung")
    image = models.ImageField(upload_to='blog_images/', verbose_name="Ảnh bìa")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Tác giả")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    views = models.IntegerField(default=0, verbose_name="Lượt xem")
    is_active = models.BooleanField(default=True, verbose_name="Hiển thị")
    
    def __str__(self):
        return self.title
    
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    class Meta:
        verbose_name = "Bài viết"
        verbose_name_plural = "Bài viết"
        ordering = ['-created_date']

class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Nội dung bình luận")
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'Bình luận bởi {self.user.username} trên {self.blog.title}'
    
    class Meta:
        verbose_name = "Bình luận"
        verbose_name_plural = "Bình luận"
        ordering = ['-created_date']

def format_price(value):
    """Helper function để format giá tiền"""
    try:
        return f"{int(value):,}₫"
    except (ValueError, TypeError):
        return "0₫"

class Promotion(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name="Tên khuyến mãi")
    code = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="Mã khuyến mãi")
    banner_image = models.ImageField(upload_to='promotion_banners/', null=True, blank=True, verbose_name="Ảnh bìa")
    card_image = models.ImageField(upload_to='promotion_cards/', null=True, blank=True, verbose_name="Ảnh thẻ khuyến mãi")
    description = models.TextField(null=True, blank=True, verbose_name="Mô tả")
    terms_conditions = models.TextField(null=True, blank=True, verbose_name="Điều kiện sử dụng")
    
    # Discount fields
    discount_type = models.CharField(
        max_length=20,
        choices=[
            ('PERCENT', 'Giảm theo phần trăm'),
            ('AMOUNT', 'Giảm theo số tiền'),
        ],
        verbose_name="Loại giảm giá"
    )
    discount_percent = models.FloatField(default=0, verbose_name="Phần trăm giảm")
    discount_amount = models.FloatField(default=0, verbose_name="Số tiền giảm")
    min_order_value = models.FloatField(default=0, verbose_name="Giá trị đơn hàng tối thiểu")
    max_discount_amount = models.FloatField(null=True, blank=True, verbose_name="Số tiền giảm tối đa")
    
    # Time and usage limits
    start_date = models.DateTimeField(verbose_name="Ngày bắt đầu")
    end_date = models.DateTimeField(verbose_name="Ngày kết thúc")
    usage_limit = models.IntegerField(default=0, verbose_name="Giới hạn sử dụng")
    used_count = models.IntegerField(default=0, verbose_name="Số lần đã sử dụng")
    is_active = models.BooleanField(default=True, verbose_name="Còn hiệu lực")
    
    @property
    def is_valid(self):
        now = timezone.now()
        return (
            self.is_active and
            self.start_date <= now and
            self.end_date >= now and
            (self.usage_limit == 0 or self.used_count < self.usage_limit)
        )
    
    @property
    def discount_display(self):
        if self.discount_type == 'PERCENT':
            return f"{self.discount_percent:.1f}%"
        return format_price(self.discount_amount)
    
    @property
    def min_order_display(self):
        return format_price(self.min_order_value)
    
    @property
    def max_discount_display(self):
        if self.max_discount_amount:
            return format_price(self.max_discount_amount)
        return None
    
    @property
    def banner_url(self):
        try:
            return self.banner_image.url
        except:
            return '/static/images/default_promotion_banner.jpg'
    
    @property
    def card_url(self):
        try:
            return self.card_image.url
        except:
            return '/static/images/default_promotion_card.jpg'
    
    @property
    def usage_percent(self):
        if self.usage_limit > 0:
            return (self.used_count / self.usage_limit) * 100
        return 0
    
    def __str__(self):
        return f"{self.title} ({self.code})"
    
    class Meta:
        verbose_name = "Khuyến mãi"
        verbose_name_plural = "Khuyến mãi"
        ordering = ['-start_date']

class PromotionUsage(models.Model):
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name='usages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    used_date = models.DateTimeField(auto_now_add=True)
    discount_amount = models.FloatField()

    class Meta:
        verbose_name = "Lịch sử sử dụng khuyến mãi"
        verbose_name_plural = "Lịch sử sử dụng khuyến mãi"
        unique_together = ['promotion', 'order']


