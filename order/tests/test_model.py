from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.utils import timezone
import datetime

from order.models import Cart, CartItem, Order, OrderItem, Transaction
from shop.models import Product
from core.tests.test_models import test_address



def test_user(email='test@mail.com', password='Test1234', extra={}):
    return get_user_model().objects.create_user(email, password, **extra)


def test_cart():
    return Cart.objects.create(user=test_user())


def test_product():
    return Product.objects.create(name='test', price=1000, quantity=1)


def test_order():
    return Order.objects.create(address=test_address(test_user()), user=test_user(email='a@m.com'))


def test_order_item():
    return OrderItem(count=1, product=test_product(), order=test_order())
    

def test_transaction():
    return Transaction.objects.create(user=test_user('b@c.com'), order=test_order(), transaction_code='1234', total_price=1)


class CartModelTest(TestCase):
    
    def test_cart_str(self):
        cart = test_cart()
        self.assertEqual(str(cart), cart.user.email)
        
        
class CartItemModelTest(TestCase):
    
    def test_cart_item_str(self):    
        cart_item = CartItem.objects.create(count=1, 
                                            cart=test_cart(),
                                            product=test_product()
                                            )
        self.assertEqual(str(cart_item), f'{cart_item.cart} : {cart_item.product}')
        
    def test_cart_item_count(self):
        with self.assertRaises(IntegrityError):
            cart_item = CartItem.objects.create(count=-1, 
                                                cart=test_cart(),
                                                product=test_product()
                                                )
            
            
class OrderModelTest(TestCase):
    
    
    def test_order_time_for_pay(self):        
        order = test_order()        
        self.assertEqual(order.time_for_pay.date(), (timezone.now() + datetime.timedelta(minutes=30)).date())
        
    def test_order_str(self):        
        order = test_order()        
        self.assertEqual(str(order), f'{order.user} : {order.status}')
        
    def test_order_status(self):        
        order = test_order()        
        self.assertEqual(order.status, '1')
        

class OrderItemModelTest(TestCase):
    
        
    def test_order_item_str(self):        
        order_item = test_order_item()        
        self.assertEqual(str(order_item), f'{order_item.order} : {order_item.product}')
        
    def test_order_item_count(self):
        with self.assertRaises(IntegrityError):
            order_item = OrderItem.objects.create(count=-1, 
                                                order=test_order(),
                                                product=test_product()
                                                )
            

class TransactionModelTest(TestCase):
    
        
    def test_transaction_str(self):        
        transaction = test_transaction()
        self.assertEqual(str(transaction), f'{transaction.user} : {transaction.transaction_code}')
        