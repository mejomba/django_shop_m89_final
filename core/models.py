import uuid
import os

from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone


def user_image_file_path(instance, filename: str):
    """generate file path for user profile image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/user/', filename)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """create and save new user"""
        print(extra_fields)
        if not email:
            raise ValueError('ایمیل اجباری است')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """create and save new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user


class BaseModel(models.Model):
    """create base model for DRY"""

    create_at = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    last_update = models.DateTimeField(verbose_name='آخرین به روز رسانی', auto_now=True)
    is_deleted = models.BooleanField(default=False)
    delete_date = models.DateTimeField(verbose_name='تاریخ حذف شدن', null=True, blank=True)

    class Meta:
        abstract = True


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """Custom user that support email instead of username"""

    USER_ROLE = (('a', 'ادمین'), ('o', 'ناظر'), ('c', 'مشتری'))
    email = models.EmailField(verbose_name='ایمیل', max_length=255, unique=True)
    phone = models.CharField(verbose_name='شماره تلفن', max_length=11)
    first_name = models.CharField(verbose_name='نام', max_length=64)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=64)
    is_active = models.BooleanField(verbose_name='فعال', default=False)
    is_staff = models.BooleanField(verbose_name='کارمند', default=False)
    role = models.CharField(verbose_name='نقش کاربر', choices=USER_ROLE, max_length=1)
    profile_image = models.ImageField(verbose_name='تصویر پروفایل', upload_to=user_image_file_path, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    @property
    def full_name(self):
        if (f := self.first_name) and (l := self.last_name):
            return f'{f} {l}'
        return f'{self.email}'


class Address(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    country = models.CharField(verbose_name='کشور', max_length=32)
    province = models.CharField(verbose_name='استان', max_length=32)
    city = models.CharField(verbose_name='شهر', max_length=32)
    street = models.CharField(verbose_name='خیابان', max_length=32)
    zip_code = models.CharField(verbose_name='کد پستی', max_length=10)
    pelak = models.CharField(verbose_name='پلاک', max_length=4)
    full_address = models.TextField(verbose_name='آدرس کامل', max_length=512)

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس ها'

    def __str__(self):
        return f'{self.user.full_name}'
