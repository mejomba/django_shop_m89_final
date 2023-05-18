from django.test import TestCase
from django.contrib.auth import get_user_model

from django.contrib.auth.models import BaseUserManager
class ModelTest(TestCase):
    
    def test_create_user_with_correct_data(self):
        
        email, password, phone, first_name, last_name = \
            'test@mail.com', 'Test1234', '09112345678', 'mojtaba', 'aminzadeh'
        
        user = get_user_model().objects.create_user(
            email = email,
            password = password,
            phone = phone,
            first_name = first_name,
            last_name = last_name
        )
        
        self.assertEqual(user.email, email)
        self.assertEqual(user.phone, phone)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.role, 'c')
        self.assertFalse(user.is_active)
        self.assertTrue(user.check_password(password))
        
        
    def test_email_normalize(self):
        email, password, phone, first_name, last_name = \
            'test@MaiL.CoM', 'Test1234', None, None, None
        
        user = get_user_model().objects.create_user(
            email = email,
            password = password,
            phone = phone,
            first_name = first_name,
            last_name = last_name
        )
        
        self.assertEqual(user.email, email.lower())
        
    def test_create_user_invalid_email(self):
        """Test user with empty email"""
        with self.assertRaises(ValueError) as invalid_mail:
            get_user_model().objects.create_user('', )
            
        self.assertEqual(str(invalid_mail.exception), 'ایمیل اجباری است')
            
    def test_create_user_invalid_phone(self):
        """Test create user with invalid phone number"""
        
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('test@mail.com', 'Test1234', phone='1')
            
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('test@mail.com', 'Test1234', phone='091123456789')
            
    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser('test@mail.com', 'Test1234')
        
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        
            