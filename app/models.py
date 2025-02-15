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
    


