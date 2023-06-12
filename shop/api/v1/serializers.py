from rest_framework import serializers

from core.models import Address
from shop.models import Product
from order.models import Cart, CartItem, Order, OrderItem
# from core.api.v1.serializers import UserSerializer
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ['password']


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        exclude = ['user']


class AddressSerializer2(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Address
        fields = '__all__'


class CreateAddressSerializer(serializers.ModelSerializer):
    # user = UserSerializer()

    class Meta:
        model = Address
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    # get_price_apply_discount = serializers.Field()
    # get_final_price = serializers.Field()

    class Meta:
        model = Product
        print('__all__')
        # fields = '__all__'
        fields = ['id', 'get_price_apply_discount', 'get_final_price', 'name', 'brand', 'price', 'thumbnail']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    # cart = CartSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'count', 'product', 'cart']


class CartSerializerWithCurrentProduct(serializers.ModelSerializer):
    user = UserSerializer()
    # cartitem_set = CartItemSerializer(many=True)
    cartitem_set = serializers.SerializerMethodField()
    current_product = ProductSerializer()

    def get_cartitem_set(self, cart):
        qs = CartItem.objects.filter(cart_id=cart, is_deleted=False)
        serializer = CartItemSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Cart
        # fields = '__all__'
        fields = ['id', 'user', 'cartitem_set', 'current_product', 'get_cart_total_price']


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # cartitem_set = CartItemSerializer(many=True)
    cartitem_set = serializers.SerializerMethodField()

    def get_cartitem_set(self, cart):
        qs = CartItem.objects.filter(cart_id=cart, is_deleted=False)
        serializer = CartItemSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Cart
        # fields = '__all__'
        fields = ['id', 'user', 'cartitem_set', 'get_cart_total_price']


class CartSerializerWithDiscount(serializers.ModelSerializer):
    user = UserSerializer()
    # cartitem_set = CartItemSerializer(many=True)
    cartitem_set = serializers.SerializerMethodField()
    get_cart_total_price = serializers.SerializerMethodField()

    def get_cartitem_set(self, cart):
        qs = CartItem.objects.filter(cart_id=cart, is_deleted=False)
        serializer = CartItemSerializer(instance=qs, many=True)
        return serializer.data

    def get_get_cart_total_price(self, obj):
        discount_code = self.context.get('discount_code')
        total_price = obj.get_cart_total_price(discount_code=discount_code)
        return total_price

    class Meta:
        model = Cart
        # fields = '__all__'
        fields = ['id', 'user', 'cartitem_set', 'get_cart_total_price']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    # cart = CartSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'count', 'product', 'order']


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    orderitem_set = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    shipping_display = serializers.SerializerMethodField()
    address_set = serializers.SerializerMethodField()
    address = AddressSerializer()
    # address = AddressSerializer()

    def get_orderitem_set(self, order):
        qs = OrderItem.objects.filter(order_id=order, is_deleted=False)
        serializer = OrderItemSerializer(instance=qs, many=True)
        return serializer.data

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_shipping_display(self, obj):
        return obj.get_shipping_display()

    def get_address_set(self, obj):
        qs = Address.objects.filter(user=obj.user, is_deleted=False)
        serializer = AddressSerializer(instance=qs, many=True)
        return serializer.data
    class Meta:
        model = Order
        # fields = ['id', 'user', 'jcreate_at', 'orderitem_set', 'get_order_total_price', 'status_display', 'shipping_display', 'address', 'time_for_pay']
        fields = ['id', 'user', 'jcreate_at', 'orderitem_set', 'get_order_total_price', 'status_display', 'shipping_display', 'address_set', 'address', 'time_for_pay']
