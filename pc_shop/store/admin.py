from django.contrib import admin
from .models import Category,Product,Order,OrderItem
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 10


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category','name','price','stock','available','created_at']
    list_filter = ['category','created_at']
    list_editable = ['stock','available']
    list_per_page = 10
    search_fields = ['category','name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','status']
    list_editable = ['status',]
    list_per_page = 10
    list_filter = ['status',]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order','product','quantity','price']
    list_per_page = 10



@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('اطلاعات اضافه', {'fields': ('phone_number', 'address')}),
    )

