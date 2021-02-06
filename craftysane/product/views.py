from django.http.response import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from eshop.models import *
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return HttpResponse('Product')

def addReview(request, id):
   url = request.META.get('HTTP_REFERER')  # get last url
   #return HttpResponse(url)
   if request.method == 'POST':  # check post
      form = ReviewForm(request.POST)
      if form.is_valid():
         data = Review()  # create relation with model
         data.rate = form.cleaned_data['rate']
         data.ip = request.META.get('REMOTE_ADDR')
         data.product_id=id
         current_user= request.user
         data.user_id=current_user.id
         data.save()  # save data to table
         messages.success(request, "Your review has ben sent. Thank you for your interest.")
         return HttpResponseRedirect(url)

   return HttpResponseRedirect(url)