from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'main'

urlpatterns = [
    # path('login/', views.login_attempt, name='login_attempt'),
    # path('login/', views.LoginAPI.as_view(), name='login'),
    # path('logout/', views.user_logout, name='logout'),
    # path('register/', views.RegisterAPI.as_view(), name='register'),
    # path('register/', views.register_attempt, name='register_attempt'),
    # path('register/', views.register, name='register'),
    # path('login/', views.user_login, name='login'),
    # path('logout/', views.user_logout, name='logout'),
    # path('token', views.token_send, name='token_send'),
    path('success/', views.success, name='success'),
    path('verify/<auth_token>/', views.verify , name="verify"),
    # path('error' , views.error_page, name="error"),
    path('forgot_password/' , views.forgot_password , name="forgot_password"),
    path('change_password/<token>/' , views.change_password , name="change_password"),
    path('your_account/', views.your_account, name='your_account'),
    path('products/', views.products, name='products'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('gifts/', views.gifts, name='gifts'),
    path('gifts/<slug:slug>/', views.gift_detail, name='gift_detail'),
    path('blogs/', views.blogs, name='blogs'),
    path('contact_us/request/', views.contact_us_receive, name='contact_us_receive'),
    path('blogs/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('products/review/<slug:slug>/', views.product_review, name='product_review'),
    path('products/review/edit/<slug:slug>/', views.product_review_edit, name='product_review_edit'),
    path('add_to_cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('add_to_wishlist/<slug:slug>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<slug:slug>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('quantity_change_cart/', views.quantity_change_cart, name='quantity_change_cart'),
    path('cart_checkout/', views.cart_checkout, name='cart_checkout'),
    # path('buy_now/<slug:slug>/', views.buy_now, name='buy_now'),
    path('process_order/', views.process_order, name='process_order'),
    path('about/', views.about, name='about'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('faqs_and_blogs/', views.faqs, name='faqs_and_blogs'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
