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

class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'discount_type', 'discount_display', 'start_date', 'end_date', 'is_active', 'is_valid')
    list_filter = ('discount_type', 'is_active', 'start_date', 'end_date')
    search_fields = ('title', 'code', 'description')
    readonly_fields = ('used_count',)
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('title', 'code', 'description', 'terms_conditions')
        }),
        ('Hình ảnh', {
            'fields': ('banner_image', 'card_image')
        }),
        ('Giảm giá', {
            'fields': ('discount_type', 'discount_percent', 'discount_amount', 'min_order_value', 'max_discount_amount')
        }),
        ('Thời gian & Giới hạn', {
            'fields': ('start_date', 'end_date', 'usage_limit', 'used_count', 'is_active')
        }),
    )

class PromotionUsageAdmin(admin.ModelAdmin):
    list_display = ('promotion', 'user', 'order', 'used_date', 'discount_amount')
    list_filter = ('used_date', 'promotion')
    search_fields = ('promotion__code', 'user__username', 'order__id')
    readonly_fields = ('used_date',)

admin.site.register(Promotion, PromotionAdmin)
admin.site.register(PromotionUsage, PromotionUsageAdmin)

@admin.register(AboutContent)
class AboutContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'content')

@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon')
    search_fields = ('title', 'description')

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone', 'email')

