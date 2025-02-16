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

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_date', 'views', 'is_active')
    list_filter = ('category', 'is_active', 'created_date')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'created_date', 'is_active')
    list_filter = ('is_active', 'created_date')
    search_fields = ('content', 'user__username', 'blog__title')

admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(BlogComment, BlogCommentAdmin)

