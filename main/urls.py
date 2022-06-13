from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'main'

urlpatterns = [
    path('verify/<auth_token>/', views.verify , name="verify"),
    path('user_details/', views.user_details , name='user_details'),
    path('forgot_password/' , views.forgot_password , name="forgot_password"),
    path('change_password/<token>/' , views.change_password , name="change_password"),
    path('your_account/', views.your_account, name='your_account'),
    path('your_account/edit/', views.account_edit, name='account_edit'),
    path('special_products/', views.special_products, name='special_products'),
    path('products/', views.products, name='products'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('gifts/', views.gifts, name='gifts'),
    path('gifts/<slug:slug>/', views.gift_detail, name='gift_detail'),
    path('blogs/', views.blogs, name='blogs'),
    path('contact_us/request/', views.contact_us_receive, name='contact_us_receive'),
    path('contact_us/gift/', views.gift_contact_us_receive, name='gift_contact_us_receive'),
    path('contact_us/product/', views.product_contact_us_receive, name='product_contact_us_receive'),
    path('blogs/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('products/review/<slug:slug>/', views.product_review, name='product_review'),
    path('products/review/edit/<slug:slug>/', views.product_review_edit, name='product_review_edit'),
    path('add_to_cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('get_full_cart/', views.get_full_cart, name='get_full_cart'),
    path('empty_cart/', views.empty_cart, name='empty_cart'),
    path('add_to_wishlist/<slug:slug>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<slug:slug>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('quantity_change_cart/', views.quantity_change_cart, name='quantity_change_cart'),
    path('cart_checkout/', views.cart_checkout, name='cart_checkout'),
    path('verify_coupon/', views.verify_coupon, name='verify_coupon'),
    path('customer_coupons/', views.customer_coupons, name='customer_coupons'),
    path('return_order/', views.return_order, name='return_order'),
    path('process_order/', views.process_order, name='process_order'),
    path('all_addresses/', views.all_addresses, name='all_addresses'),
    path('change_default_address/', views.change_default_address, name='change_default_address'),
    path('add_address/', views.add_address, name='add_address'),
    path('delete_address/', views.delete_address, name='delete_address'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('global_reviews/', views.global_reviews, name='global_reviews'),
    path('maker_class_reviews/', views.maker_class_reviews, name='maker_class_reviews'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
