from django.db import models # type: ignore
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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
    Customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
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
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    mobile = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    

class CheckoutOrder(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Chờ xử lý'),
        ('PROCESSING', 'Đang xử lý'),
        ('SHIPPING', 'Đang giao hàng'),
        ('COMPLETED', 'Đã hoàn thành'),
        ('CANCELLED', 'Đã hủy'),
    ]

    PAYMENT_CHOICES = [
        ('COD', 'Thanh toán khi nhận hàng'),
        ('BANK', 'Chuyển khoản ngân hàng'),
        ('PAYPAL', 'PayPal'),
    ]

    # Liên kết với User và Order
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    
    # Thông tin cá nhân
    full_name = models.CharField(max_length=200, verbose_name="Họ và tên")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=15, verbose_name="Số điện thoại")
    
    # Thông tin giao hàng
    address = models.CharField(max_length=255, verbose_name="Địa chỉ")
    city = models.CharField(max_length=100, verbose_name="Thành phố")
    district = models.CharField(max_length=100, verbose_name="Quận/Huyện")
    ward = models.CharField(max_length=100, verbose_name="Phường/Xã")
    
    # Thông tin thanh toán
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='COD',
        verbose_name="Phương thức thanh toán"
    )
    
    # Trạng thái đơn hàng
    order_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name="Trạng thái đơn hàng"
    )
    
    # Thông tin bổ sung
    notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú")
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Tổng tiền"
    )
    
    # Thời gian
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Cập nhật lần cuối")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Đơn hàng Checkout"
        verbose_name_plural = "Đơn hàng Checkout"

    def __str__(self):
        return f"Đơn hàng #{self.id} - {self.customer.username}"

    def get_full_address(self):
        return f"{self.address}, {self.ward}, {self.district}, {self.city}"

    def get_status_display_name(self):
        return dict(self.STATUS_CHOICES)[self.order_status]

    def get_payment_method_display_name(self):
        return dict(self.PAYMENT_CHOICES)[self.payment_method]

    
