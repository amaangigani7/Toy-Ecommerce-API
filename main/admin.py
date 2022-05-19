from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.forms import TextInput, Textarea
# Register your models here.

class UserAdminConfig(UserAdmin):
    model = Customer
    search_fields = ('email', 'user_name', 'first_name',)
    list_filter = ('email', 'user_name', 'first_name', 'is_active', 'is_staff')
    ordering = ('-created_at',)
    list_display = ('email', 'user_name', 'first_name', 'is_active', 'is_staff')

    fieldsets = (
        (None, {'fields':('email', 'user_name', 'first_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about', )})
    )

    formfield_overrides = {
        Customer.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(Customer, UserAdminConfig)
admin.site.register(Blog)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Gift)
admin.site.register(Coupon)
admin.site.register(GiftImage)

class CartItemAdminConfig(admin.ModelAdmin):
    list_display = ['customer', 'product', 'quantity']

admin.site.register(CartItem, CartItemAdminConfig)

class OrderAdminConfig(admin.ModelAdmin):
    list_display = ['customer', 'transaction_id', 'complete', 'delivered', 'shipping_method']

admin.site.register(Order, OrderAdminConfig)

class OrderItemAdminConfig(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity']

admin.site.register(OrderItem, OrderItemAdminConfig)


class ShippingAddressAdminConfig(admin.ModelAdmin):
    list_display = ['customer', 'phone_number', 'first_name', 'default_add']

admin.site.register(ShippingAddress, ShippingAddressAdminConfig)
admin.site.register(WishList)

class ProductReviewAdminConfig(admin.ModelAdmin):
    list_display = ['customer', 'product', 'review']

admin.site.register(ProductReview, ProductReviewAdminConfig)

class ContactUsAdminConfig(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'message']

admin.site.register(ContactUs, ContactUsAdminConfig)
