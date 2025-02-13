from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Category)

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city']
    search_fields = ['user__username', 'user__email', 'phone']
    list_filter = ['city']

