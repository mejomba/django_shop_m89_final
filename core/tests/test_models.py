from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError


def test_user(email='test@mail.com', password='Test1234', extra={}):
    return get_user_model().objects.create_user(email, password, **extra)


class ModelTest(TestCase):
    
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
        