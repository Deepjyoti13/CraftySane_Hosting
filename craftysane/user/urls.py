from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
#app_name = 'user'
urlpatterns = [
    path('', views.index, name='user_index'),
    path('update/', views.user_update, name='user_update'),
    path('login/', views.login_form, name='login_form'),
    path('logout/', views.logout_func, name='logout_func'),
    path('signup_form/', views.form, name='signup_form'),
    path("otp/<str:pk>", views.otp, name="otp"),

    path('orders/', views.user_orders, name='user_orders'),
    path('orders_product/', views.user_order_product, name='user_order_product'),
    path('orderdetail/<int:id>', views.user_orderdetail, name='user_orderdetail'),
    path('order_product_detail/<int:id>/<int:oid>', views.user_order_product_detail, name='user_order_product_detail'),
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(template_name="user/password_reset.html"),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="user/password_reset_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="user/password_reset_form.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="user/password_reset_done.html"
        ),
        name="password_reset_complete",
    ),
    # path('comments/', views.user_comments, name='user_comments'),
    # path('deletecomment/<int:id>', views.user_deletecomment, name='user_deletecomment'),

]