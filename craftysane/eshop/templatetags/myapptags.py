from eshop.models import Setting
from django import template
from django.urls import reverse
from craftysane import settings
from order.models import *
from product.models import *
from eshop.models import *

register = template.Library()

a=0
@register.filter
def increment(value, arg):
    global a
    a = (a+1)
    return a

@register.simple_tag
def reset():
    global a
    a=0

@register.simple_tag
def categorylist():
    return Category.objects.all()

@register.simple_tag
def shopcartcount(userid):
    count = ShopCart.objects.filter(user_id=userid).count()
    return count

@register.simple_tag
def wishlistcount(userid):
    count = WishList.objects.filter(user_id=userid).count()
    return count

@register.simple_tag
def settingslist():
    return Setting.objects.all().last()