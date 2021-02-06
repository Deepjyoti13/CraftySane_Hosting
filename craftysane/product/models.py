from django.db import models
from django.db.models import Avg, Count
from django.db.models.expressions import F
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.


class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey(
        'self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    keywords = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    status = models.CharField(max_length=20, choices=STATUS)
    slug = models.SlugField(null=True, unique=True)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    feature = models.BooleanField(default=False)
    featimage = models.ImageField(upload_to='Carousel/', null=True, blank=True)
    deal = models.BooleanField(default=False)
    minimum_Offer = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):                           # __str__ method elaborated later in
        # post.  use __unicode__ in place of
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),

    )

    DEALS = (
        ('Deal of the day', 'Deal of the day'),
        ('Deal of the week', 'Deal of the week'),
        ('Deal of the month', 'Deal of the month'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='child', related_query_name='child')
    brand_name = models.CharField(max_length=50)
    title = models.CharField(max_length=150)
    keywords = models.TextField()
    assured = models.BooleanField(default=False, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    prevprice = models.FloatField()
    price = models.FloatField()
    variant = models.CharField(max_length=20, choices=VARIANTS, default='None')
    dealActive = models.BooleanField(default=False)
    deals = models.CharField(max_length=30, choices=DEALS, default='None')
    amount = models.IntegerField()
    minamount = models.IntegerField()
    detail = RichTextUploadingField()
    status = models.CharField(max_length=20, choices=STATUS)
    slug = models.SlugField()
    dealSlug = models.SlugField()
    featured = models.BooleanField(default=False)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})
    
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.dealSlug})

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    def avaregereview(self):
        reviews = Review.objects.filter(
            product=self, status='True').aggregate(average=Avg('rate'))
        avg = 0
        if reviews["average"] is not None:
            avg = float(reviews["average"])
        return avg

    def countreview(self):
        reviews = Review.objects.filter(
            product=self, status='True').aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

    @property
    def offer(self):
        import math
        return math.ceil((((self.prevprice - self.price)*100/self.prevprice) / 1000) * 1000)

    image_tag.short_description = 'Image'

class Deal(models.Model):
    CHOICES = (
        ('Deal of the day', 'Deal of the day'),
        ('Deal of the week', 'Deal of the week'),
        ('Deal of the month', 'Deal of the month'),
    )
    active = models.BooleanField(default=False)
    image = models.ImageField(upload_to='Deals/', null='True')
    deal = models.CharField(
        max_length=25, choices=CHOICES, null=True, blank=True)
    onlyChar1 = models.CharField(max_length=10, unique=True, null=True)
    onlyChar2 = models.CharField(max_length=10, unique=True, null=True)
    start = models.DateField(auto_now_add=False)
    end = models.DateField(auto_now_add=False)
    dealSlug = models.SlugField()
    def __str__(self):
        return self.deal
    
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.dealSlug})

class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    class Meta:
        verbose_name_plural = "Images"

    def __str__(self):
        return self.title

class Review(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # subject = models.CharField(max_length=50, blank=True)
    # comment = models.CharField(max_length=250,blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rate']

class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""

class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(
        Color, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(
        Size, on_delete=models.CASCADE, blank=True, null=True)
    image_id = models.IntegerField(blank=True, null=True, default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            varimage = img.image.url
        else:
            varimage = ""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""

class Offer(models.Model):
    category = models.ForeignKey(
        Category, related_name='offer', on_delete=models.CASCADE)
    off = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    show = models.BooleanField(default=False)
    image = models.ImageField(upload_to='Offers', null=True)

    def __str__(self):
        return self.name
