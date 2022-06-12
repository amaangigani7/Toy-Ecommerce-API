from rest_framework import serializers
from rest_framework.response import Response
from .models import *
import uuid

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class MakerClassReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MakerClassReview
        fields = '__all__'

class GlobalReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalReview
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('id', 'email', 'user_name', 'first_name', 'last_name', 'about', 'created_at', 'is_active')


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ('author', 'title', 'content', 'posted_at', 'image_link', 'slug')

class ContactUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactUs
        fields = '__all__'

class ProductReviewSerializer(serializers.ModelSerializer):
    # customer = CustomerSerializer()

    class Meta:
        model = ProductReview
        fields = ('id', 'by', 'product', 'rating', 'review', 'edited_on')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image_link')

class SimilarProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimilarProduct
        fields = ('id', 'slug')
#
# def find_wishlisted(slug, user):
#     # for i in WishList.objects.filter(customer=user):
#     #     print(i)
#     # print(Product.objects.get(slug=slug))
#     if user != "None":
#         if Product.objects.get(slug=slug) in WishList.objects.filter(customer=user):
#             return True
#     else:
#         return False

class ProductSerializer(serializers.ModelSerializer):
    get_image_url = ProductImageSerializer(many=True)
    get_reviews = ProductReviewSerializer(many=True)
    get_product_rating = serializers.FloatField()
    get_similar_products = SimilarProductSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

    # def get_is_wishlisted(self, obj):
    #     try:
    #         return find_wishlisted(obj.slug, self.context['request'].user)
    #     except:
    #         return find_wishlisted(obj.slug, "None")

class SpecialProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = SpecialProduct
        fields = '__all__'


class GiftImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftImage
        fields = ('id', 'image_link')


class GiftSerializer(serializers.ModelSerializer):
    get_image_url = GiftImageSerializer(many=True)

    class Meta:
        model = Gift
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    customer = CustomerSerializer()

    class Meta:
        model = CartItem
        fields = '__all__'


class WishListSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    customer = CustomerSerializer()

    class Meta:
        model = WishList
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'image_link', 'product_name', 'quantity', 'product_slug',
                    'get_total', 'placed_on', 'item_status', 'returned', 'refunded')


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    get_order_items = OrderItemSerializer(many=True)
    shipping_address = ShippingAddressSerializer()

    class Meta:
        model = Order
        fields = '__all__'



# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100, min_length=6)
    user_name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    # class Meta:
    #     model = User
    #     fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
    #
    # def validate(self, args):
    #     email = args.get('email', None)
    #     username = args.get('username', None)
    #     if User.objects.filter(email=email).exists():
    #         raise serializers.ValidationError({'email': ('email already exists')})
    #     if User.objects.filter(username=username).exists():
    #         raise serializers.ValidationError({'username': ('username already exists')})
    #     return super().validate(args)
    #
    # def create(self, validated_data):
    #     return User.objects.create_user(**validated_data)
    #
    class Meta:
        model = Customer
        fields = ('id', 'user_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # print('validated_data= ', validated_data)
        while True:
            auth_token = str(uuid.uuid4())
            if not Customer.objects.filter(verification_token=auth_token).first():
                break
        customer = Customer.objects.create(user_name=validated_data['user_name'], email=validated_data['email'], verification_token=auth_token)
        customer.set_password(validated_data['password'])
        customer.save()
        return customer
