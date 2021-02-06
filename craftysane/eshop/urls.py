from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.index, name="home"),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('deals/<str:slug>', views.deals, name="deals"),
    path('contact/', views.contactus, name="contact"),
    path('category/<int:id>/<slug:slug>', views.category_products, name="category_product"),
    path('special-deals/<int:id>/<slug:slug>', views.category_offer, name="category_offer"),
    path('search/', views.search, name='search'),
    path('search_auto/', views.search_auto, name='search_auto'),
    path('ajaxcolor/', views.ajaxcolor, name='ajaxcolor'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)