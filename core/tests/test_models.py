from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.utils import timezone

from core.models import Address, Discount


def test_user(email='test@mail.com', password='Test1234', extra={}):
    return get_user_model().objects.create_user(email, password, **extra)


def test_address(user, extra={}):
    return Address.objects.create(user=user, **extra)


def test_discount(extra):
    return Discount.objects.create(**extra)


class UserModelTest(TestCase):
    
    def test_create_user_with_complet_data(self):
        
        extra = {'phone': '09112345678', 
                'first_name': 'mojtaba', 
                'last_name': 'aminzadeh'}
        
        user = test_user(extra=extra)
        
        self.assertEqual(user.email, 'test@mail.com')
        self.assertEqual(user.phone, extra['phone'])
        self.assertEqual(user.first_name, extra['first_name'])
        self.assertEqual(user.last_name, extra['last_name'])
        self.assertEqual(user.role, 'c')
        self.assertFalse(user.is_active)
        self.assertTrue(user.check_password('Test1234'))
        
        
    def test_email_normalize(self):
        required = ('test@MaiL.CoM', 'Test1234')
        user = test_user(*required)
        
        self.assertEqual(user.email, required[0].lower())
        
    def test_create_user_invalid_email(self):
        """Test user with empty email"""
        with self.assertRaises(ValueError) as invalid_mail:
            get_user_model().objects.create_user('', )
            
        self.assertEqual(str(invalid_mail.exception), 'ایمیل اجباری است')
    
    def test_user_fullname_property(self):
        extra = {'first_name': 'mojtaba', 'last_name': 'aminzadeh'}
        user = test_user(extra=extra)
        self.assertEqual(user.full_name, 'mojtaba aminzadeh')
        
    def test_create_user_invalid_phone(self):
        """Test create user with invalid phone number"""
        
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('test@mail.com', 'Test1234', phone='1')
            
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('test@mail.com', 'Test1234', phone='091123456789')
        
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('test@mail.com', 'Test1234', phone='0911234567a')
            
    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser('test@mail.com', 'Test1234')
        
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        
    def test_user_email_exist(self):
        """Test user with exist email (maybe not compatible with postgresql)"""
        user = test_user()
        with self.assertRaises(IntegrityError):
            new_user = get_user_model().objects.create_user(user.email, 'Test1234')
            
    def test_user_phone_exist(self):
        """Test user with exist phone (maybe not compatible with postgresql)"""
        
        extra = {'phone': '09112345678'}
        user = test_user(extra=extra)
        
        with self.assertRaises(IntegrityError):
            new_user = get_user_model().objects.create_user('new@mail.com', 'Test1234', phone=user.phone)
    
    def test_user_str(self):
        user = test_user()
        self.assertEqual(user.email, 'test@mail.com')
        
        
class AddressModelTest(TestCase):
    
    def test_address_str(self):
        extra = {'country':'ایران',
                'province': 'تهرا',
                'city': 'شهر',
                'street': 'خیابان',
                'zip_code': '1234567890',
                'pelak': '1234',
                'full_address': 'آدرس کامل شامل یک متن',}
        
        address = test_address(user=test_user(), extra=extra)
        self.assertEqual(str(address), address.user.full_name)
        

class DiscountModelTest(TestCase):
    
    def setUp(self) -> None:
        self.extra = {'percent': '10', 
                    'mablagh': '1000', 
                    'start_date': timezone.now(), 
                    'end_date': timezone.now()+timezone.timedelta(1)}
        
    def test_discount_str(self):
        
        discount = Discount.objects.create(name='test', code='1234', **self.extra)
        self.assertEqual(str(discount), discount.code)
        
    def test_discount_unique_name(self):
        
        discount = Discount.objects.create(name='test', code='1234', **self.extra)
        with self.assertRaises(IntegrityError):
            Discount.objects.create(name='test', code='4321', **self.extra)
            
    def test_discount_unique_code(self):
        
        discount = Discount.objects.create(name='test1', code='1234', **self.extra)
        with self.assertRaises(IntegrityError):
            Discount.objects.create(name='test2', code='1234', **self.extra)
            
    def test_discount_percent_mablagh_pair(self):
        
        self.extra.pop('percent')
        self.extra.pop('mablagh')
        with self.assertRaises(IntegrityError):
            discount = Discount.objects.create(name='test1', code='1234', **self.extra)
