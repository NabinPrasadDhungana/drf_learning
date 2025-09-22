from django.contrib import admin
from .models import Product, Order, OrderItem

# Register your models here.
admin.site.register(Product)

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)