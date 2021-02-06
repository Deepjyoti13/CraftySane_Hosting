from django.urls import path
from . import views
urlpatterns = [
    # path('', views.index, name="Order"),
    path('addtoshopcart/<int:id>', views.addtoshopcart, name="addtoshopcart"),
    path('addtowishlist/<int:id>', views.addtowishlist, name="addtowishlist"),
    path('deletefromcart/<int:id>', views.deletefromcart, name="deletefromcart"),
    path('deletefromlist/<int:id>', views.deletefromlist, name="deletefromlist"),
    path('shopcart/', views.shopcart, name="shopcart"),
    path('wishlist/', views.wishlist, name="wishlist"),
    path('cancel-order/<int:id>', views.cancelorder, name="cancelorder"),
    path('return-order/<int:id>', views.returnorder, name="returnorder"),
    path('orderproduct/', views.orderproduct, name='payu_demo'),
    path('cod/', views.cashondelivery, name='cod'),
    path('success', views.payu_success, name='success'),
    path('failure', views.payu_failure, name='failure'),
]