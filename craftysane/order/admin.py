from django.contrib import admin
from .models import *
# Register your models here.
class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'price', 'amount' ]
    list_filter = ['user']
class OrderProductline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product','price','quantity','amount')
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'paid', 'phone','city','total', 'status', 'code', 'mode']
    list_filter = ['status', 'paid', 'mode']
    search_fields = ['code', 'ZIP', 'first_name', 'phone', 'city', 'status', 'mode']
    readonly_fields = ('user', 'first_name', 'last_name', 'phone', 'address','city','country', 'city','total', 'ip')
    can_delete = False
    inlines = [OrderProductline]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product','price','quantity','amount']
    list_filter = ['user']

admin.site.register(ShopCart,ShopCartAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)