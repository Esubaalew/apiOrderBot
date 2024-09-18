from django.contrib import admin
from .models import Order, Product


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('id', 'product', 'full_name', 'address', 'phone_number', 'comment', 'quantity', 'order_date')
    list_filter = ('product', 'full_name', 'address', 'phone_number', 'comment', 'quantity', 'order_date')
    search_fields = ('product', 'full_name', 'address', 'phone_number', 'comment', 'quantity', 'order_date')
    ordering = ('-order_date',)


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('id', 'name', 'description', 'image', 'price', 'date_added')
    list_filter = ('name', 'price', 'date_added')
    search_fields = ('name', 'price', 'date_added')
    ordering = ('-date_added',)


admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)


# change the title and header of the admin site
admin.site.site_header = "Store Administration"
admin.site.site_title = "Shop Admin Portal"
admin.site.index_title = "Welcome to the Shop Admin  Dashboard"
