from product.models import *
from order.models import *
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from user.forms import *
from django.utils.crypto import get_random_string
from django.conf import settings
from paywix.payu import Payu
from django.views.decorators.csrf import csrf_exempt
from product.models import *
from decimal import Decimal

MERCHANT_KEY = '7RMI_B8Qxc43LG2S'
payu_config = settings.PAYU_CONFIG
merchant_key = payu_config.get('merchant_key')
merchant_salt = payu_config.get('merchant_salt')
surl = payu_config.get('success_url')
furl = payu_config.get('failure_url')
mode = payu_config.get('mode')
payu = Payu(merchant_key, merchant_salt, surl, furl, mode)

@login_required(login_url='/user/login')
def addtoshopcart(request,id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    product= Product.objects.get(pk=id)

    if product.variant != 'None':
        variantid = request.POST.get('variantid')  # from variant add to cart
        checkinvariant = ShopCart.objects.filter(variant_id=variantid, user_id=current_user.id)  # Check product in shopcart
        if checkinvariant:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""
    else:
        checkinproduct = ShopCart.objects.filter(product_id=id, user_id=current_user.id) # Check product in shopcart
        if checkinproduct:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control==1: # Update  shopcart
                if product.variant == 'None':
                    data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
                else:
                    data = ShopCart.objects.get(product_id=id, variant_id=variantid, user_id=current_user.id)
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else : # Inser to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id =id
                if product.variant != 'None':
                    data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product added to Shopcart ")
        return HttpResponseRedirect(url)

    else: # if there is no post
        if control == 1:  # Update  shopcart
            data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()  #
        else:  #  Inser to Shopcart
            data = ShopCart()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.variant_id =None
            data.save()  #
        messages.success(request, "Product added to Shopcart")
        return HttpResponseRedirect(url)

def shopcart(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total=0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += float(rs.product.price * rs.quantity)
        else:
            total += float(rs.variant.price * rs.quantity)
    #return HttpResponse(str(total))
    context={'shopcart': shopcart,
             'category':category,
             'total': total,
             }
    return render(request,'eshop/shopcart.html',context)

@login_required(login_url='/user/login')  # Check login
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item is deleted form Shopcart.")
    return HttpResponseRedirect("/order/shopcart")

def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += float(rs.product.price * rs.quantity)
        else:
            total += float(rs.variant.price * rs.quantity)
            
    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        # return HttpResponse(request.POST.items())
        if form.is_valid():
            order = Order()
            order.key = request.user.id
            order.mode = 'PREPAY'
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.address = form.cleaned_data['address']
            order.city = form.cleaned_data['city']
            order.state = form.cleaned_data['state']
            order.ZIP = form.cleaned_data['ZIP']
            order.country = form.cleaned_data['country']
            order.phone = form.cleaned_data['phone']
            order.user_id = current_user.id
            order.total = total
            order.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()  # random cod
            order.code = ordercode
            order.save()
            
            # data = { 'amount': str(order.total), 
            # 'firstname': order.first_name, 
            # 'email': request.user.email,
            # 'phone': order.phone, 'productinfo': 'test', 
            # 'lastname': order.last_name, 'address1': order.address, 
            # 'address2': str(order.key), 'city': order.city, 
            # 'state': str(order.state), 'country': order.country, 
            # 'zipcode': str(order.ZIP), 'udf1': '', 
            # 'udf2': '', 'udf3': '', 'udf4': '', 'udf5': '',
            # }
            
            data = { 'amount': str(order.total), 
            'firstname': order.first_name, 
            'email': request.user.email,
            'phone': order.phone, 'productinfo': 'test', 
            'lastname': 'test', 'address1': 'test', 
            'address2': order.key, 'city': 'test', 
            'state': 'test', 'country': 'test', 
            'zipcode': 'tes', 'udf1': '', 
            'udf2': '', 'udf3': '', 'udf4': '', 'udf5': ''
        }
            
            # data = {'amount': str(order.total),
            # 'firstname': order.first_name,
            # 'email': request.user.email,
            # 'phone': order.phone, 'productinfo': 'Our product',
            # 'lastname': order.last_name, 'address1': order.address,
            # 'address2': order.address, 'city': order.city,
            # 'state': order.state, 'country': order.country,
            # 'zipcode': order.ZIP, 'udf1': '',
            # 'udf2': '', 'udf3': '', 'udf4': '', 'udf5': ''
            # }
            txnid = ordercode
            data.update({"txnid": txnid})
            payu_data = payu.transaction(**data)
            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = order.id  # Order Id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                # detail.price = rs.product.price
                if rs.product.variant == 'None':
                    detail.price = float(rs.product.price)
                else:
                    detail.price = float(rs.variant.price)
                detail.variant_id   = rs.variant_id
                detail.amount = rs.amount
                detail.save()
                # ***Reduce quantity of sold product from Amount of Product
                
                if  rs.product.variant=='None':
                    product = Product.objects.get(id=rs.product_id)
                    product.amount -= rs.quantity
                    product.save()
                else:
                    variant = Variants.objects.get(id=rs.product_id)
                    variant.quantity -= rs.quantity
                    variant.save()
                
                # product = Product.objects.get(id=rs.product_id)
                # product.amount -= rs.quantity
                # product.save()

                # ************ <> *****************
            # Clear & Delete shopcart

            return render(request, 'order/payu_checkout.html', {"posted": payu_data})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")
    form = OrderForm()
    profile = UserProfile.objects.filter(user_id=current_user.id)
    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               'form': form,
               'profile': profile,
               }
    return render(request, 'order/order_form.html', context)

@csrf_exempt
def payu_success(request):
    print("success")
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu.verify_transaction(data)
    # print("Request:")
    # print(request.POST)
    # print("DATA: ")
    # print(data["txnid"])
    ShopCart.objects.filter(user_id=data["address2"]).delete()
    request.session['cart_items'] = 0
    order = Order.objects.get(code = data["txnid"])
    order.paid = True
    order.save()
    return render(request, 'order/order_completed.html', {"ordercode": data["txnid"]})

@csrf_exempt
def payu_failure(request):
    print("failure")
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu.verify_transaction(data)
    return render(request, 'order/order_failed.html', {"ordercode": data["txnid"]})

def wishlist(request):
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = WishList.objects.filter(user_id=current_user.id)
    # shipping > ZIP 799000 to 799250 shipping = 0;
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
    # return HttpResponse(str(total))
    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               }
    return render(request, 'eshop/wishlist.html', context)

def addtowishlist(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    product = Product.objects.get(pk=id)
    checkinproduct = WishList.objects.filter(
        product_id=id, user_id=current_user.id)  # Check product in shopcart
    if checkinproduct:
        control = 1  # The product is in the cart
    else:
        control = 0  # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        form = WishListForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update  shopcart
                data = WishList.objects.get(
                    product_id=id, user_id=current_user.id)
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else:  # Inser to Shopcart
                data = WishList()
                data.user_id = current_user.id
                data.product_id = id
                # data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.save()
        else:
            print(form.errors)
        messages.success(request, "Product added to Wish List ")
        return HttpResponseRedirect(url)

    else:  # if there is no post
        if control == 1:  # Update  shopcart
            data = WishList.objects.get(product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()  #
        else:  # Inser to Shopcart
            data = WishList()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            # data.variant_id =None
            data.save()  #
        messages.success(request, "Product added to Wish List")
        return HttpResponseRedirect(url)

@login_required(login_url='/user/login')  # Check login
def deletefromlist(request, id):
    WishList.objects.filter(id=id).delete()
    messages.success(request, "Your item is deleted form Wish List.")
    return HttpResponseRedirect("/order/wishlist")

def cashondelivery(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += float(rs.product.price * rs.quantity)
        else:
            total += float(rs.variant.price * rs.quantity)

    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        #return HttpResponse(request.POST.items())
        if form.is_valid():
            data = Order()
            data.mode = 'COD'
            data.first_name = form.cleaned_data['first_name'] #get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.ZIP = form.cleaned_data['ZIP']
            data.country = form.cleaned_data['country']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode= get_random_string(5).upper() # random cod
            data.code =  ordercode
            data.save() #


            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id     = data.id # Order Id
                detail.product_id   = rs.product_id
                detail.user_id      = current_user.id
                detail.quantity     = rs.quantity
                if rs.product.variant == 'None':
                    detail.price    = rs.product.price
                else:
                    detail.price = rs.variant.price
                detail.variant_id   = rs.variant_id
                detail.amount        = rs.amount
                detail.save()
                # ***Reduce quantity of sold product from Amount of Product
                if  rs.product.variant=='None':
                    product = Product.objects.get(id=rs.product_id)
                    product.amount -= rs.quantity
                    product.save()
                else:
                    variant = Variants.objects.get(id=rs.product_id)
                    variant.quantity -= rs.quantity
                    variant.save()
                #************ <> *****************

            ShopCart.objects.filter(user_id=current_user.id).delete() # Clear & Delete shopcart
            request.session['cart_items']=0
            messages.success(request, "Your Order has been completed. Thank you ")
            return render(request, 'order/cod_completed.html',{'ordercode':ordercode,'category': category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form= OrderForm()
    profile = UserProfile.objects.filter(user_id=current_user.id)
    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               'form': form,
               'profile': profile,
               }
    return render(request, 'order/order_form.html', context)

def returnorder(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    order = Order.objects.get(id = id)
    order.status = 'Return Requested'
    order.save()
    return HttpResponseRedirect(url)

def cancelorder(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    order = Order.objects.get(id = id)
    order.status = 'Canceled'
    order.save()
    return HttpResponseRedirect(url)
