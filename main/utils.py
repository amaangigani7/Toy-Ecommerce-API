from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from os import listdir
from main.models import *
import pandas as pd
import os

def get_create_address(address, user, parameter="both"):
    if parameter == 'both':
        new_add, created = ShippingAddress.objects.get_or_create(
            customer = user,
            first_name = address['first_name'],
            last_name = address['last_name'],
            address_1 = address['address_1'],
            address_2 = address['address_2'],
            city = address['city'],
            state = address['state'],
            zipcode = address['zipcode'],
            country = address['country'],
            phone_number = address['phone_number']
        )
        return new_add, created
    elif parameter == 'get':
        try:
            print('entered elif')
            new_add = ShippingAddress.objects.filter(
                customer = user,
                first_name = address['first_name'],
                last_name = address['last_name'],
                address_1 = address['address_1'],
                address_2 = address['address_2'],
                city = address['city'],
                state = address['state'],
                zipcode = address['zipcode'],
                country = address['country'],
                phone_number = address['phone_number']
            ).first()
        except:
            new_add = None
        return new_add


def send_email_after_registration(email, token):
    subject = 'Your email needs to be verified'
    message = 'Hi paste the link to verify your account https://srushtigosai123.pythonanywhere.com/main/verify/{}'.format(token)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail(subject, message, email_from, recipient_list)

def send_email_for_password_reset(email, token):
    subject = 'Reset your password here'
    message = 'Hi, click on the link to reset your password https://srushtigosai123.pythonanywhere.com/main/change_password/{}'.format(token)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail(subject, message, email_from, recipient_list)

def send_email_after_purchase(order):
    subject = 'Order Placed Successfully'
    message = 'Hi, Your order has been placed for {} of amount {}'.format(order.get_order_items, order.get_order_total)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [order.customer.email,]
    send_mail(subject, message, email_from, recipient_list)

def check_coupon(coupon, user):
    dis = 0
    c = Coupon.objects.filter(is_active=True)
    for i in c:
        if i.name == coupon and (i.customer == user or i.customer == None):
            print("you get a discount of {}%".format(i.discount))
            dis = i.discount
            break
    return dis

# order, created = Order.objects.get_or_create(customer__user_name='amaan35', complete=False)
# order.save()
# total = 0
# for i in CartItem.objects.filter(customer__user_name='amaan35'):
#     order_item, created = OrderItem.objects.get_or_create(order=order, product=i.product)
#     cart_quan = CartItem.objects.get(customer__user_name='amaan35', product=i.product)
#     order_item.quantity = cart_quan.quantity
#     order_item.save()
#     # breakpoint()
#     total += order_item.get_total()

# DO NOT USE THIS FOR IMAGE UPLOAD
# folder_dir = 'F:\\udemy.django\\toy_ecommerce\\ecom\\products'
# for i in os.listdir(folder_dir):
#     if i.endswith('.csv') or i.endswith('.zip'):
#         pass
#     else:
#         for j in os.listdir(folder_dir + '\\' + i):
#             if j.endswith(".jpg"):
#                 img = ProductImage()
#                 img.product = Product.objects.get(name=i)
#                 img.image = settings.MEDIA_ROOT '\\' + j
#                 img.save()


# p = pd.read_csv('F:\\udemy.django\\toy_ecommerce\\ecom\\products\\Products.csv')
# for i in range(len(p['Product Name'])):
#     c = Product()
#     c.name = p['Product Name'][i]
#     c.description = p['Description'][i]
#     c.meta_description = p['Meta Description'][i]
#     c.short_description = p['Short Description'][i]
#     c.sale_price = "{0:.2f}".format(float(p['Sale Price'][i]))
#     c.product_price = "{0:.2f}".format(float(p['Product Price'][i]))
#     c.on_sale = p['Is Sale On'][i]
#     c.strip_menu = p[' As Per Strip Menu'][i]
#     c.mega_menu = p['As Per Mega Menu'][i]
#     c.slug = p['Slug'][i]
#     c.tags = p['Tags'][i]
#     c.save()
