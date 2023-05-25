from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.utils import timezone
import datetime

from core.models import Address
from order.models import Cart, CartItem, Order, OrderItem, Transaction
from shop.models import Product


class CartModelTest(TestCase):
    def setUp(self) -> None:
        self.test_user = get_user_model().objects.create_user('test@mail.com', 'Test1234')
        self.test_cart = Cart.objects.create(user=self.test_user)
    
    def test_cart_str(self):
        cart = self.test_cart
        self.assertEqual(str(cart), cart.user.email)
        
        
class CartItemModelTest(TestCase):
    def setUp(self) -> None:
        self.test_user = get_user_model().objects.create_user('test@mail.com', 'Test1234')
        self.test_cart = Cart.objects.create(user=self.test_user)
        self.test_product = Product.objects.create(name='test', price=1000, quantity=1)

    def test_cart_item_str(self):
        cart_item = CartItem.objects.create(count=1,
                                            cart=self.test_cart,
                                            product=self.test_product
                                            )
        self.assertEqual(str(cart_item), f'{cart_item.cart} : {cart_item.product}')

    def test_cart_item_count(self):
        with self.assertRaises(IntegrityError):
            CartItem.objects.create(count=-1,
                                    cart=self.test_cart,
                                    product=self.test_product
                                    )
            
            
class OrderModelTest(TestCase):
    def setUp(self) -> None:
        self.test_user = get_user_model().objects.create_user('test@mail.com', 'Test1234')
        self.test_address = Address.objects.create(user=self.test_user)
        self.test_order = Order.objects.create(address=self.test_address, user=self.test_user)
    
    def test_order_time_for_pay(self):
        order = self.test_order
        self.assertEqual(order.time_for_pay.date(), (timezone.now() + datetime.timedelta(minutes=30)).date())
        
    def test_order_str(self):        
        order = self.test_order
        self.assertEqual(str(order), f'{order.user} : {order.status}')
        
    def test_order_status(self):        
        order = self.test_order
        self.assertEqual(order.status, '1')
        

class OrderItemModelTest(TestCase):
    def setUp(self) -> None:
        self.test_user = get_user_model().objects.create_user('test@mail.com', 'Test1234')
        self.test_product = Product.objects.create(name='test', price=1000, quantity=1)
        self.test_address = Address.objects.create(user=self.test_user)
        self.test_order = Order.objects.create(address=self.test_address, user=self.test_user)
        self.test_order_item = OrderItem(count=1, product=self.test_product, order=self.test_order)

    def test_order_item_str(self):
        order_item = self.test_order_item
        self.assertEqual(str(order_item), f'{order_item.order} : {order_item.product}')

    def test_order_item_count(self):
        with self.assertRaises(IntegrityError):
            order_item = OrderItem.objects.create(count=-1,
                                                  order=self.test_order,
                                                  product=self.test_product
                                                  )


class TransactionModelTest(TestCase):
    def setUp(self) -> None:
        self.test_user = get_user_model().objects.create_user('test@mail.com', 'Test1234')
        self.test_address = Address.objects.create(user=self.test_user)
        self.test_order = Order.objects.create(address=self.test_address, user=self.test_user)
        self.test_transaction = Transaction.objects.create(user=self.test_user, order=self.test_order, transaction_code='1234', total_price=1)

    def test_transaction_str(self):
        transaction = self.test_transaction
        self.assertEqual(str(transaction), f'{transaction.user} : {transaction.transaction_code}')
