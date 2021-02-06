from django import http
from django.db.models.query_utils import PathInfo, subclasses
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib import messages
import json
from .models import *
from product.models import *
from .forms import *
from django.db.models import Q
import math
# Create your views here.
def error_404_view(request, exception):
    return render(request, 'eshop/404.html')


def index(request):
    setting = Setting.objects.all().last()
    category = Category.objects.all()
    # men = Category.objects.get(title = 'Men')
    # child = men.get_children()
    deal = Deal.objects.filter(active=True)
    product_slider = Category.objects.filter(feature = True)
    product_picked = Product.objects.all().filter(
        featured=True).order_by('-id')[:4]
    product_trending = Product.objects.all().order_by('?')[:6]
    page = 1
    print(page)
    print(request.user.username)
    context = {'setting': setting, 'page': page, 'category': category, 'product_slider': product_slider, 'range': range(
        1, len(product_slider)), 'product_picked': product_picked, 'product_trending': product_trending, 'deal': deal, # 'men': men, 'child': child
               }
    return render(request, 'eshop/index.html', context)

def deals(request, slug):
    deal = Deal.objects.get(active = True, dealSlug = slug)
    product = Product.objects.filter(dealActive=True, dealSlug = slug)
    context = {
        'deal': deal,
        'products': product,
        'len': len(product)
    }
    return render(request, 'eshop/deals.html', context)

def aboutus(request):
    return HttpResponse('About Us')

def contactus(request):
    category = Category.objects.all()
    if request.method == 'POST':  # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()  # create relation with model
            data.name = form.cleaned_data['name']  # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.phone = form.cleaned_data['phone']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save data to table
            messages.success(
                request, "Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')
    setting = Setting.objects.all().last()
    form = ContactForm
    context = {'setting': setting, 'form': form, 'category': category}
    return render(request, 'eshop/contactus.html', context)

class Accumulator:

    def __init__(self, start=0):
        self.reset(start)

    def increment(self, step=1):
        step = 1 if not isinstance(step, int) else step
        self.count += step
        return self.count

    def reset(self, start=0):
        start = 0 if not isinstance(start, int) else start
        self.count = start
        return self.count

def category_products(request, id, slug):
    catdata = Category.objects.get(pk=id)
    if catdata.is_leaf_node():
        # print("Leaf")
        products = Product.objects.filter(category_id=id) 
        context = {
                'products': products,
                'catdata': catdata,
                'count': Accumulator(),
               }
        # print(products)
    else:
        subcat = Category.objects.filter(parent_id=id)
        # print("Not Leaf")
        
        products = Product.objects.filter(category__parent_id=id).order_by('?')
        # print(products)
        context = {
               'products': products,
               'catdata': catdata,
               'subcat': subcat,
               'len': len(products),
               'count': Accumulator(),
               }

    return render(request, 'eshop/category_products.html', context)

def category_offer(request, id, slug):
    catdata = Category.objects.get(pk=id)
    products = Product.objects.filter(Q(category__parent_id=id) | Q(category_id=id))
        
    context = {
               'products': products,
               'catdata': catdata,
               }
    for i in products:
        print(i.offer>=catdata.minimum_Offer)
    return render(request, 'eshop/category_offers.html', context)

def search(request):
    if request.method == 'POST':  # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']  # get form input data
            if len(query) > 300:
                products = Product.objects.none()
            else:
                title = Product.objects.filter(title__icontains=query)
                brand = Product.objects.filter(brand_name__icontains=query)
                keywords = Product.objects.filter(keywords__icontains=query)
                category = Product.objects.filter(category__title__icontains=query)
                products = title.union(brand, keywords, category)
                if products.count() == 0:
                    messages.error(
                            request, "No search results found. Please refine your search!")
            category = Category.objects.all()
            context = {'products': products, 'query': query,
                       'category': category, 'len': len(products) }
            return render(request, 'eshop/search_products.html', context)
    return HttpResponseRedirect('/')

def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        title = Product.objects.filter(title__icontains=q)
        brand = Product.objects.filter(brand_name__icontains=q)
        keywords = Product.objects.filter(keywords__icontains=q)
        category = Product.objects.filter(category__title__icontains=q)
        products = title.union(brand, keywords, category)
        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def product_detail(request,id,slug):
    query = request.GET.get('q')
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    subcat = Category.objects.filter(child__id=id)
    for i in subcat:
        prod = Product.objects.filter(category_id = i.id).exclude(id=id)
        print(prod)
    # print(list(subcat))
    images = Images.objects.filter(product_id=id)
    context = {'product': product,'category': category,
               'images': images, 'range': range(1, (len(images)+1)), 'prod': prod,
               }
    if product.variant !="None": # Product have variants
        if request.method == 'POST': #if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id) #selected product by click color radio
            colors = Variants.objects.filter(product_id=id,size_id=variant.size_id )
            sizes = Variants.objects.raw('SELECT DISTINCT * FROM  product_variants WHERE product_id=%s ORDER BY size_id',[id])
            # sizes = Variants.objects.raw('SELECT * FROM  product_variants WHERE product_id=%s GROUP BY size_id',[id])
            query += variant.title+' Size:' +str(variant.size) +' Color:' +str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id,size_id=variants[0].size_id )
            # sizes = Variants.objects.raw('SELECT * FROM  product_variants WHERE product_id=%s GROUP BY size_id',[id])
            sizes = Variants.objects.raw('SELECT DISTINCT * FROM  product_variants WHERE product_id=%s ORDER BY size_id',[id])
            variant =Variants.objects.get(id=variants[0].id)
        context.update({'sizes': sizes, 'colors': colors,
                        'variant': variant,'query': query
                        })
    # print(product.countreview())
    return render(request,'eshop/products.html',context)

def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('eshop/color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)
