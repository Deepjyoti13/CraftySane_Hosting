from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import *
import admin_thumbnails

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'status']
    list_filter = ['status']
    prepopulated_fields = {'slug': ('title',)}
    
class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}
    # inlines = [CategoryLangInline]
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'
@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 7
    
@admin_thumbnails.thumbnail('image')
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image','title','image_thumbnail']

class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'image_tag']
    list_filter = ['category', 'status', ]
    readonly_fields = ('image_tag',)
    search_fields = ['title', 'category',]
    inlines = [ProductImageInline, ProductVariantsInline ]
    prepopulated_fields = {'slug': ('title',), 'dealSlug': ('deals',)}
    
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'rate', 'status','create_at']
    list_filter = ['status', 'rate', ]
    readonly_fields = ('ip','user','product','rate','id')

class ColorAdmin(admin.ModelAdmin):
    list_display = ['name','code','color_tag']
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name','code']
class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title','product','color','size','price','quantity','image_tag']

class DealsAdmin(admin.ModelAdmin):
    list_display = ['deal','start','end', 'active']
    list_filter = ['active', ]
    prepopulated_fields = {'dealSlug': ('deal',)}


admin.site.register(Category, CategoryAdmin2)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(Variants,VariantsAdmin)
admin.site.register(Deal, DealsAdmin)