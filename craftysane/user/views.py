from django.http.response import HttpResponse
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core import signing
import random
from .forms import *
from .models import *
from order.models import *
from product.models import *
# Create your views here.


def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            # userprofile = UserProfile.objects.get(user_id=current_user.id)
            # request.session['userimage'] = userprofile.image.url

            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.warning(
                request, "Login error!! Username or password is incorrect")
            return HttpResponseRedirect('/login')
    # Return an 'invalid login' error message.
    #category = Category.objects.all()
    context = {  # 'category': category
    }
    return render(request, 'user/login_form.html', context)

@login_required(login_url='/user/login')  # Check login
def index(request):
    #category = Category.objects.all()
    current_user = request.user  # Access User Session information
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {  # 'category': category,
        'profile': profile}
    return render(request, 'user_profile.html', context)

def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')

def form(request):
    x = random.randrange(100000, 1000000)
    User = get_user_model()
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.warning(request, "Signup error!! Invalid email or email already taken")
            else: 
                user = form.save()
                user.is_active = False
                rand = x
                user.save()
                try:
                    send_mail(
                    'Your OTP is provided below. You are one step away from enrolling yourself!',#email heading
                    str(x),#email body
                    'expresstotell@gmail.com',#email sender
                    [email],#receivers email
                    fail_silently=False,
                    )
                except:
                    #if email sending failed
                    messages.info(request, "Can not send email. Enter a valid email or check your internet connection.")
                    return redirect('signup_form')
                # if email sending was successfull
                # dumping the id for improving security           
                value = signing.dumps({"id": user.id, "rand": rand})
                return redirect('otp', value)
            
    context = {'form': form}
    return render(request, 'user/signup_form.html', context)

def otp(request, pk):
    #loading the primary key 
    signing.loads(pk)
    d = signing.loads(pk)
    # query
    reg = User.objects.get(id=d['id'])
    if request.method == "POST":
        # if the onetime password given by the user is right 
        if d['rand'] == int(request.POST.get('onetime')):

            # status is changed to True which by default is false 
            reg.is_active = True

            # generating registration number 
            rand= random.randrange(100000, 1000000)
            reg.save()

            return redirect('login_form')

        else:
            # if otp is wrong delete data from database  and redirect to form
            reg.delete()
            # reg.user.delete()
            messages.info(request, "Invalid OTP. Try again!")
            return redirect('signup_form')
    # for rendering html
    return render(request, 'user/otp.html')

@login_required(login_url='/user/login')  # Check login
def user_update(request):
    if request.method == 'POST':
        # request.user is user  data
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        # "userprofile" model -> OneToOneField relatinon with user
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)

@login_required(login_url='/login') # Check login
def user_orders(request):
    #category = Category.objects.all()
    current_user = request.user
    orders=Order.objects.filter(user_id=current_user.id).order_by('-id')
    context = {#'category': category,
               'orders': orders,
               }
    return render(request, 'user/user_orders.html', context)

@login_required(login_url='/login') # Check login
def user_orderdetail(request,id):
    #category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        #'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user/user_order_details.html', context)

@login_required(login_url='/login') # Check login
def user_order_product(request):
    #category = Category.objects.all()
    current_user = request.user
    order_product = OrderProduct.objects.filter(user_id=current_user.id).order_by('-id')
    context = {#'category': category,
               'order_product': order_product,
               }
    return render(request, 'user/user_order_products.html', context)

@login_required(login_url='/login') # Check login
def user_order_product_detail(request,id,oid):
    #category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id,user_id=current_user.id)
    context = {
        #'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user/user_order_detail.html', context)
