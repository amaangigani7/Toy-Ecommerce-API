from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.template.defaultfilters import slugify
import random
from datetime import datetime, timedelta
# Create your models here.

class CustomAccountManager(BaseUserManager):

    def create_user(self, email, user_name, password, **other_fields):
        if not email:
            raise ValueError(gettext_lazy('You must enter an email'))
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, user_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError('Super User must have "is_staff=True"')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Super User must have "is_superuser=True"')
        return self.create_user(email, user_name, password, **other_fields)


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(gettext_lazy('email_address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    # start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(gettext_lazy('about'), max_length=500, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    forget_password_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name',]

    def __str__(self):
        return self.user_name


class Blog(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    slug = models.SlugField(unique=True, null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posted_at']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.slug == '' or self.slug is None:
            self.slug = slugify(self.title)
            self.save()
        return self.title


class Product(models.Model):
    sale_choices = ((True, "YES"), (False, "NO"))

    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    sale_price = models.DecimalField(null=True, blank=True, max_digits=100, decimal_places=2)
    product_price = models.DecimalField(null=True, blank=True, max_digits=100, decimal_places=2)
    on_sale = models.BooleanField(default='NO', choices=sale_choices)
    category = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(null=False, unique=True)
    strip_menu = models.CharField(max_length=200, null=True, blank=True)
    mega_menu = models.TextField(null=True, blank=True)
    tags = models.TextField(null=True, blank=True)
    in_stock = models.BooleanField(default=True, null=True, blank=True)
    skills_and_learnings = models.TextField(null=True, blank=True)
    real_life_connect = models.TextField(null=True, blank=True)
    technical_details = models.TextField(null=True, blank=True)

    @property
    def get_product_rating(self):
        reviews = self.get_reviews
        l = len(reviews)
        s = 0
        for i in reviews:
            s += int(i.rating)
        return s

    @property
    def get_image_url(self):
        image_urls = self.productimage_set.all()
        # breakpoint()
        # total = sum([item.get_total for item in order_items])
        return image_urls

    @property
    def get_reviews(self):
        reviews = self.productreview_set.all()
        return reviews

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.FileField(null=True, blank=True)

    @property
    def image_url(self):
        try:
            url = 'http://127.0.0.1:8000' + self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.product.name

class ProductReview(models.Model):
    RATING_CHOICES = ((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'))

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(choices=RATING_CHOICES, null=True)
    review = models.TextField(unique=True)
    edited_on = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = [['customer', 'product']]

    def __str__(self):
        return "{}'s review on {}".format(self.customer.user_name, self.product.name)


class Gift(models.Model):
    sale_choices = ((True, "YES"), (False, "NO"))

    name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    description = models.TextField(null=True, blank=True)
    sale_price = models.DecimalField(null=True, blank=True, max_digits=100, decimal_places=2)
    product_price = models.DecimalField(null=True, blank=True, max_digits=100, decimal_places=2)
    on_sale = models.BooleanField(default='NO', choices=sale_choices)
    category = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(null=True, unique=True, blank=True)

    @property
    def get_image_url(self):
        image_urls = self.giftimage_set.all()
        return image_urls

    def __str__(self):
        if self.slug is None:
            self.slug = slugify(self.name)
            self.save()
        return self.name

class GiftImage(models.Model):
    gift = models.ForeignKey(Gift, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.FileField(null=True, blank=True)

    def __str__(self):
        return str(self.gift) + "'s image object"

class ContactUs(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = PhoneNumberField()
    message = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = 'Contact Us'
        ordering = ['-sent_on']


class CartItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = [['customer', 'product']]

    def __str__(self):
        return "{}'s cart".format(self.customer.user_name)


class WishList(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = [['customer', 'product']]

    def __str__(self):
        return "{}'s wishlist".format(self.customer.user_name)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(null=True, max_length=100)
    last_name = models.CharField(null=True, max_length=100)
    address_1 = models.CharField(null=True, max_length=255)
    address_2 = models.CharField(null=True, blank=True, max_length=255)
    city = models.CharField(null=True, max_length=255)
    state = models.CharField(null=True, max_length=10)
    zipcode = models.CharField(null=True, max_length=100)
    country = models.CharField(null=True, max_length=50)
    phone_number = PhoneNumberField(null=True, )
    date_added = models.DateTimeField(auto_now_add=True)
    default_add = models.BooleanField(null=True, blank=True, default=False)

    class Meta:
        unique_together = ('customer', 'first_name', 'last_name', 'address_1', 'address_1', 'city', 'state', 'zipcode', 'country', 'phone_number')


    def __str__(self):
        if self.address_1 is None:
            return str(self.id)
        else:
            return self.address_1


class Order(models.Model):
    delivered_choices = ((True, "YES"), (False, "NO"))

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(null=True, blank=True, max_length=255)
    delivered = models.BooleanField(default=False, choices=delivered_choices)
    shipping_method = models.CharField(null=True, blank=True, max_length=255)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = [['customer', 'transaction_id']]
        ordering = ['-transaction_id', '-id']

    @property
    def get_order_total(self):
        # breakpoint()
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_order_items(self):
        order_items = self.orderitem_set.all()
        return order_items

    def __str__(self):
        if self.complete == True:
            return str(self.transaction_id)
        else:
            return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['order', 'product']]

    @property
    def get_total(self):
        return self.product.sale_price * self.quantity

    def change_address(self, new_add):
        return new_add

    def __str__(self):
        return self.product.name

class Coupon(models.Model):
    name = models.CharField(max_length=10)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    discount = models.IntegerField(validators=[MinValueValidator(1),
                                       MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
