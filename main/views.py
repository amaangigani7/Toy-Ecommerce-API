from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import status, authentication, permissions, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Q
from .models import *
from .utils import *
from .forms import *
from .serializers import *
from django.core import serializers
from django.utils import timezone
import random
import uuid
import datetime
import json
import razorpay

# Create your views here.
def home(request):
    return render(request, 'main/home.html')

@api_view(['GET'])
def special_products(request):
    sp = SpecialProduct.objects.all()
    serializer = SpecialProductSerializer(sp, many=True)
    return Response({'special_products': serializer.data})

@api_view(['GET'])
def global_reviews(request):
    gr = GlobalReview.objects.all()
    serializer = GlobalReviewSerializer(gr, many=True)
    return Response({'global_reviews': serializer.data})

@api_view(['GET'])
def maker_class_reviews(request):
    mcr = MakerClassReview.objects.all()
    serializer = MakerClassReviewSerializer(mcr, many=True)
    return Response({'maker_class_reviews': serializer.data})


@api_view(['GET'])
def products(request):
    if request.user.is_authenticated:
        products = Product.objects.all()
        wishlisted = []
        non_wishlisted = []
        for i in WishList.objects.filter(customer=request.user):
            wishlisted.append(i.product)
        for i in products:
            if i not in wishlisted:
                non_wishlisted.append(i)
        serializer_1 = ProductSerializer(non_wishlisted, many=True)
        serializer_2 = ProductSerializer(wishlisted, many=True)
        print(wishlisted)
        print(non_wishlisted)
        return Response({'wishlisted': serializer_1.data, 'non_wishlisted': serializer_2.data})
    else:
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({'non_wishlisted': serializer.data})


@api_view(['GET'])
def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    img_lis = ProductImage.objects.filter(product=product)
    serializer = ProductSerializer(product)
    return Response({'product': serializer.data})

@api_view(['GET'])
def gifts(request):
    gifts = Gift.objects.all()
    serializer = GiftSerializer(gifts, many=True)
    return Response({'all_gifts': serializer.data})


@api_view(['GET'])
def gift_detail(request, slug):
    gift = Gift.objects.get(slug=slug)
    serializer = GiftSerializer(gift)
    return Response({'gift': serializer.data})


@api_view(['GET'])
def blogs(request):
    blogs = Blog.objects.all()
    serializer = BlogSerializer(blogs, many=True)
    return Response({'all_blogs': serializer.data})


@api_view(['GET'])
def blog_detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    serializer = BlogSerializer(blog)
    return Response({'blog_details': serializer.data})

@api_view(['POST'])
def contact_us_receive(request):
    name = request.data.get('name')
    email = request.data.get('email')
    phone = request.data.get('phone')
    message = request.data.get('message')
    # try:
    cu = ContactUs.objects.create(name=name, email=email, phone=phone, message=message)
    msg = "Request has been sent"
    serializer = ContactUsSerializer(cu)
    return Response({'msg': msg, 'request': serializer.data})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def product_review(request, slug):
    product = Product.objects.get(slug=slug)
    text = request.data.get('review')
    rating = request.data.get('rating')
    try:
        order_list = Order.objects.filter(customer=request.user)
        for i in order_list:
            # print("i: ", i, "order_items: ", i.get_order_items)
            for j in i.get_order_items:
                # print("j.product: ", j.product)
                if product == j.product:
                    # print('product order found!')
                    try:
                        pr = ProductReview.objects.create(customer=request.user, product=product, review=text, rating=rating)
                        pr.save()
                        msg = "Review Posted."
                    except:
                        msg = "Review Already present try editing the existing one."
    except:
        # print('you have not ordered the item to review')
        return Response({"msg": msg})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def product_review_edit(request, slug):
    product = Product.objects.get(slug=slug)
    text = request.data.get('review')
    rating = request.data.get('rating')
    pr = ProductReview.objects.get(customer=request.user, product=product)
    pr.review = text
    pr.rating = rating
    pr.edited_on = timezone.now()
    pr.save()
    msg = "Review Edited."
    return Response({"msg": msg})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def account_edit(request):
    customer = Customer.objects.get(user_name=request.user)
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    about = request.data.get('about')
    customer.first_name = first_name
    customer.last_name = last_name
    customer.about = about
    customer.save()
    msg = "Account details edited."
    return Response({"msg": msg, 'new_data': CustomerSerializer(customer).data})

# @login_required
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def cart_checkout(request):
    order, created = Order.objects.get_or_create(customer=request.user, ordered=False)
    order.save()
    cart_items = CartItem.objects.filter(customer=request.user)
    if len(cart_items) > 0:
        for i in cart_items:
            order_item, created = OrderItem.objects.get_or_create(order=order, product=i.product)
            cart_quan = CartItem.objects.get(customer=request.user, product=i.product)
            order_item.quantity = cart_quan.quantity
            order_item.save()
        total = order.get_order_total
        serializer = OrderSerializer(order)
        return Response({"order_details": serializer.data, 'total': total, 'total_paise': int(total*100)})
    else:
        msg = "The Cart is Empty"
        return Response({'msg': msg})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def verify_coupon(request):
    coupon = request.data.get('coupon')
    discount = check_coupon(coupon, request.user)
    if discount == 0:
        msg = 'Coupon is not valid for you'
    else:
        msg = '{}'.format(discount)
    return Response({'msg': msg})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def customer_coupons(request):
    coupons = Coupon.objects.filter(customer=request.user)
    if len(coupons) > 0:
        serializer = CouponSerializer(coupons, many=True)
        return Response({'coupons': serializer.data})
    else:
        return Response({'msg': "No coupons found!"})



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def process_order(request):
    try:
        address = request.data.get('address')
        shipping_method = request.data.get('shipping_method')
        order_total = request.data.get('order_total')
        coupon_code = request.data.get('coupon')
        print(order_total)
        if len(coupon_code) > 1:
            dis = check_coupon(coupon_code, request.user)
        else:
            dis = 0
        transaction_id = datetime.datetime.now().timestamp()
        try:
            order, created = Order.objects.get_or_create(customer=request.user, ordered=False)
            final_bill = order.get_order_total * (100- dis) / 100
            print(final_bill)
            if str(order_total) == str(final_bill):
                shipping_add, created = get_create_address(address, request.user)
                shipping_add.save()
                order.shipping_address = shipping_add
                order.transaction_id = transaction_id
                client = razorpay.Client(auth=("rzp_test_5Eo5eGr8zKCjKA", "5DwlU0Sb80HkKQVdYbG1ckyV"))
                DATA = {
                    # "amount": int(str(order.get_order_total)[:-3]),
                    "amount": int(final_bill),
                    "currency": "INR",
                    'payment_capture': '1'
                }
                payment = client.order.create(data=DATA)
                print(payment)
                order.ordered = True
                order.save()
                send_email_after_purchase(order)
                msg = 'order placed!'
                cart_items = CartItem.objects.filter(customer=request.user)
                for i in cart_items:
                    i.delete()
                serializer = OrderSerializer(order)
                return Response({'msg': msg, 'order_details': serializer.data})
            else:
                msg = "There was some error with provided total and actual total"
                return Response({'msg': msg})
        except:
            return Response({'msg': "Order is not created yet."})
    except ObjectDoesNotExist as e:
        return Response({'msg': e})

# breakpoint()
# try:
#     shipping_add = ShippingAddress.objects.get(customer=request.user)
# except:
#     shipping_add = ShippingAddress.objects.create(customer=request.user, order=order)
#     # shipping_add.save()
# shipping_add.first_name = first_name
# shipping_add.last_name = last_name
# shipping_add.address_1 = address_1
# shipping_add.address_2 = address_2
# shipping_add.city = city
# shipping_add.state = state
# shipping_add.zipcode = zipcode
# shipping_add.country = country
# shipping_add.phone_number = phone_number



@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_address(request):
    msg = 'adding an address'
    address = request.data.get('address')
    curr_add = ShippingAddress.objects.filter(customer=request.user, default_add=True)
    try:
        new_add, created = get_create_address(address, request.user)
        if len(curr_add) == 0:
            new_add.default_add = True
            new_add.save()
        if created == False:
            msg = "found an address"
        return Response({'msg': msg, "new_address": ShippingAddressSerializer(new_add).data, 'curr_add': ShippingAddressSerializer(curr_add, many=True).data})
    except IntegrityError:
        msg = "same address already exists"
    return Response({'msg': msg, 'curr_add': ShippingAddressSerializer(curr_add).data})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def delete_address(request):
    address = request.data.get('address')
    try:
        # add = get_create_address(address, request.user, 'get')
        add = ShippingAddress.objects.get(id=address['id'])
        if add == None:
            msg = "given address is not found"
            return Response({'msg': msg})
        add.delete()
        msg = "found and deleted the address"
        return Response({'msg': msg})
    except:
        return Response({'msg': "something went wrong"})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def all_addresses(request):
    all_addresses = ShippingAddress.objects.filter(customer=request.user)
    if len(all_addresses) > 0:
        serializer = ShippingAddressSerializer(all_addresses, many=True)
        return Response({'msg': 'All saved addresses are here', "all_addresses": serializer.data})
    else:
        return Response({'msg':'No Addresses were found for this user'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_default_address(request):
    address = request.data.get('new_address')
    msg = 'trying...'
    curr_add = ShippingAddress.objects.filter(customer=request.user, default_add=True)
    new_add, created = get_create_address(address, request.user)
    if created == False:
        msg = 'using old address'
        if new_add.default_add == True:
            msg = 'both adds are same'
        else:
            msg = 'new address made default'
    else:
        msg = 'making new address'
    new_add.default_add = True
    new_add.save()
    if len(curr_add) == 1:
        curr_add[0].default_add = False
        curr_add[0].save()
    # curr_add = ShippingAddress.objects.filter(customer=request.user, default_add=True)
    # serializer = ShippingAddressSerializer(curr_add, many=True)
    return Response({'msg': msg, "new_address": ShippingAddressSerializer(new_add).data})


@api_view(['POST'])
def subscribe(request):
    email = request.data.get('email')
    subcribe, created = Subscriber.objects.get_or_create(email=email)
    if created == False:
        return Response({'msg': 'You are already subscribed'})
    else:
        return Response({'msg': 'Your email has been added to the subscriber list'})


@api_view(['POST'])
def unsubscribe(request):
    email = request.data.get('email')
    try:
        subcriber = Subscriber.objects.get(email=email)
        subcriber.delete()
        return Response({'msg': 'You have been unsubscribed'})
    except:
        return Response({'msg': "No subscription found to unsubscribe"})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_to_cart(request, slug):
    product = Product.objects.get(slug=slug)
    try:
        c = CartItem.objects.get(customer=request.user, product=product)
        c.quantity += 1
        c.save()
    except:
        c = CartItem()
        c.customer = request.user
        c.product = product
        c.quantity = 1
        c.save()

    # print(c)
    cart = CartItem.objects.filter(customer=request.user)
    total = 0
    for i in cart:
        total += i.item_total()
    msg = "{} added to {}'s cart. Current Quantity: {}".format(c.product.name, request.user, c.quantity)
    cart_serializer = CartItemSerializer(cart, many=True)
    return Response({'msg': msg, 'full_cart': cart_serializer.data, "total": total})
    # return Response({'cart_item': cart_item_serializer.data, 'full_cart': cart_serializer.data})
    # return Response({'message': 'product found.'})

    # products = Product.objects.all()
    # msg = 'Item has been added to cart'
    # data = list(json.dumps(msg)) + list(serializers.serialize('json', products))
    # return HttpResponse(data, content_type="application/json")


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def empty_cart(request):
    cart = CartItem.objects.filter(customer=request.user)
    for i in cart:
        i.delete()
    return Response({'msg': "Cart emptied!"})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_full_cart(request):
    cart = CartItem.objects.filter(customer=request.user)
    if len(cart) < 1:
        return Response({'msg': "cart empty!"})
    else:
        total = 0
        for i in cart:
            total += i.item_total()
        cart_serializer = CartItemSerializer(cart, many=True)
        msg = 'Cart found!'
        return Response({'msg': msg, 'full_cart': cart_serializer.data, 'total': total})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_to_wishlist(request, slug):
    product = Product.objects.get(slug=slug)
    try:
        w = WishList.objects.get_or_create(customer=request.user, product=product)
        msg = "Already in {}'s wishlist".format(request.user)
    except:
        w = WishList.objects.get(customer=request.user)
        w.product = product
        w.save()
        msg = "{}'s wishlist updated".format(request.user)
    wishlist_item = WishList.objects.filter(customer=request.user)
    serializer = WishListSerializer(wishlist_item, many=True)
    return Response({'msg': msg, 'full_wishlist': serializer.data})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def remove_from_wishlist(request, slug):
    product = Product.objects.get(slug=slug)
    try:
        w = WishList.objects.get(customer=request.user, product=product)
        w.delete()
        msg = "Deleted from {}'s wishlist".format(request.user)
    except:
        msg = "Not present in {}'s wishlist".format(request.user)
    wishlist_item = WishList.objects.filter(customer=request.user)
    serializer = WishListSerializer(wishlist_item, many=True)
    return Response({'msg': msg, 'full_wishlist': serializer.data})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def quantity_change_cart(request):
    slug = request.data.get('product_slug')
    operation = request.data.get('operation')
    product = Product.objects.get(slug=slug)
    c = CartItem.objects.get(customer=request.user, product=product)
    if operation == "+":
        c.quantity += 1
        c.save()
    if operation == "-":
        c.quantity -= 1
        if c.quantity <= 0:
            c.delete()
        else:
            c.save()
    cart = CartItem.objects.filter(customer=request.user)
    # img_lis = ProductImage.objects.filter(product=product)
    # serializer = ProductSerializer(product)
    # img_serializer = ProductImageSerializer(img_lis, many=True)
    # cart_item_serializer = CartItemSerializer(c)
    msg = "{} quantity changed to {}".format(c.product.name, c.quantity)
    cart_serializer = CartItemSerializer(cart, many=True)
    return Response({'msg': msg, 'full_cart': cart_serializer.data})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def return_order(request):
    pk = request.data.get('pk')
    order = Order.objects.filter(pk=pk)
    if len(order) == 1:
        curr_order = order[0]
        if request.user == curr_order.customer:
            curr_order.returned = True
            curr_order.save()
            msg = "Your order has been returned"
        else:
            msg = "You can only return your orders."
    else:
        msg = "Order could not be fetched."
    return Response({'msg': msg})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def your_account(request):
    # print(request.user)
    # cart_items = CartItem.objects.filter(customer=request.user)
    wish_list = WishList.objects.filter(customer=request.user)
    past_orders = Order.objects.filter(customer=request.user, delivered=True)
    upcoming_orders = Order.objects.filter(customer=request.user, delivered=False)
    returned_orders = Order.objects.filter(customer=request.user, returned=True)
    # print(cart_items)
    # print(orders)
    # product = Product.objects.get(slug=slug)
    # img_lis = ProductImage.objects.filter(product=product)
    # serializer = CartItemSerializer(cart_items, many=True)
    serializer = WishListSerializer(wish_list, many=True)
    # cart_return = serializer.data
    # if len(orders) > 0:
    p_serializer = OrderSerializer(past_orders, many=True)
    u_serializer = OrderSerializer(upcoming_orders, many=True)
    r_serializer = OrderSerializer(returned_orders, many=True)
    # orders_return = o_serializer.data
    # print(serializer)
    # o_serializer = OrderSerializer(orders)
    # print(o_serializer)
    # print(serializer.data)
    # img_serializer = ProductImageSerializer(img_lis, many=True)
    # return Response({'cart_items': serializer.data})
    # 'order_details': o_serializer.data, 'cart_items': serializer.data
    return Response({
        'message': "this is your account - {}".format(request.user),
        'past_orders': p_serializer.data,
        'upcoming_orders': u_serializer.data,
        'returned_orders': r_serializer.data,
        'wish_list': serializer.data
        })
    # all_objects = list(orders) + list(cart_items)
    # data = serializers.serialize('json', all_objects)
    # return HttpResponse(data)
    # return render(request, 'main/your_account.html', {'customer': request.user, 'cart_items': cart_items, 'orders': orders})

# def about(request):
#     return render(request, 'main/about.html')
#
# def faqs(request):
#     return render(request, 'main/faqs_and_blogs.html')
#
# def contact_us(request):
#     return render(request, 'main/contact_us.html')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, customer):
        token = super().get_token(customer)

        # Add custom claims
        token['user_name'] = customer.user_name
        token['email'] = customer.email
        token['password'] = customer.password
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# class LoginAPI(TokenObtainPairView):
#     permission_classes = (permissions.AllowAny,)
#
#     def post(self, request, format=None):
#         # serializer = AuthTokenSerializer(data=request.data)
#         # serializer.is_valid(raise_exception=True)
#         # parameter = serializer.validated_data['username']
#         # password = serializer.validated_data['password']
#         # print(parameter, password)
#         parameter = request.data['email']
#         password = request.data['password']
#         print(parameter, password)
#         if parameter is None:
#             return Response({"message": 'User not found / Incorrect password'})
#         elif password is None:
#             return Response({"message": 'User not found / Incorrect password'})
#         try:
#             customer = Customer.objects.get(email=parameter)
#         except:
#             customer = Customer.objects.get(user_name=parameter)
#         print('customer active: ', customer.is_active)
#         if not customer.is_active:
#             return Response({"message": 'Profile is not verified check your mail.'})
#         print(password, customer.check_password(password))
#         if customer.check_password(password):
#             login(request, customer)
#         else:
#             return Response({"message": 'User not found / Incorrect password.'})
#         return super(LoginAPI, self).post(request, format=None)
#

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        if '.' in request.data['user_name']:
            return Response({"message": 'Username cannot have a "."'})
        if Customer.objects.filter(user_name=request.data['user_name']):
            return Response({"message": 'Username taken!'})
        if Customer.objects.filter(user_name=request.data['email']):
            return Response({"message": 'Email already registered! Try logging in!'})
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            # serializer.save()
            customer = serializer.save()
            send_email_after_registration(request.data['email'], token=Customer.objects.get(user_name=request.data['user_name']).verification_token)
            return Response({
            "status": status.HTTP_200_OK,
            "user": CustomerSerializer(customer, context=self.get_serializer_context()).data,
            "message": 'An Email has been sent to your email ID if it was valid.'
            })
        return Response({"Errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# def success(request):
#     return render(request , 'main/success.html')


# def token_send(request):
#     return render(request , 'main/token_send.html')

@api_view(['GET'])
def verify(request, auth_token):
    try:
        print(auth_token)
        customer = Customer.objects.filter(verification_token=auth_token).first()
        if customer:
            if customer.is_active:
                return Response({'message': "Your account is already verified."})
            customer.is_active = True
            customer.verification_token = None
            customer.save()
            return Response({'message': "Your account has now been verified."})
        else:
            return Response({'message': "Could not verify your registration."})
    except Exception as e:
        return Response({'message': e})



# @login_required
# def user_logout(request):
#     logout(request)
#     return render(request,'main/home.html')

@api_view(['POST'])
def change_password(request, token):
    try:
        customer = Customer.objects.filter(forget_password_token=token).first()
        if request.method == 'POST':
            new_password = request.data.get('new_password')
            confirm_password = request.data.get('confirm_password')
            parameter = request.data.get('username')
            if parameter is None:
                return Response({'message': 'Username/Email not relevant!'})
            if new_password != confirm_password:
                return Response({'message': 'New password does not match the confirm password field!'})
            try:
                try:
                    customer = Customer.objects.get(user_name=parameter)
                except:
                    customer = Customer.objects.get(email=parameter)
                customer.set_password(new_password)
                customer.forget_password_token = None
                customer.save()
                return Response({'message': 'Password has been changed!'})
            except:
                return Response({'message': 'Password could not be changed! Error in Username/Email!'})
    except Exception as e:
        return Response({'message': e})

@api_view(['POST'])
def forgot_password(request):
    try:
        parameter = request.data.get('username')
        # if not Customer.objects.filter(user_name=parameter).first() and not Customer.objects.filter(email=parameter).first():
        #     messages.success(request, 'No User found with this username')
        #     return render(request, 'main/forgot_password.html')
        try:
            try:
                customer = Customer.objects.get(user_name=parameter)
            except:
                customer = Customer.objects.get(email=parameter)
            while True:
                token = str(uuid.uuid4())
                if not Customer.objects.filter(forget_password_token=token).first():
                    break
            customer.forget_password_token = token
            customer.save()
            send_email_for_password_reset(customer.email, customer.forget_password_token)
            return Response({'message': "An email is sent to your email id"})
        except:
            return Response({'message': "No User found with this username or email"})
    except Exception as e:
        return Response({'message': e})
