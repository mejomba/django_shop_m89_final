from typing import Any
import uuid
import os
import re

from django.db.models import Q
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.html import format_html
from django.contrib.auth.models import Group

from extension.utils import to_jalali


def user_image_file_path(instance, filename: str):
    """generate file path for user profile image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/user/', filename)


class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        """create and save new user"""

        if not email:
            raise ValueError('ایمیل اجباری است')
        
        pattern = r'^09[0-9]{9}$'        
        if extra_fields.get('phone') and not re.match(pattern, extra_fields.get('phone')):
            raise ValueError('فرمت تلفن اشتباه است')
            
        user = self.model(email=self.normalize_email(email), **extra_fields)
        
        user.set_password(password)
        # if not user.role:
        #     user.role = 'c'
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
        
    def jlast_update(self):
        return to_jalali(self.last_update)    
    jlast_update.short_description = 'آخرین به روز رسانی'

    def jcreate_at(self):
        return to_jalali(self.create_at)
    jlast_update.short_description = 'تاریخ ایجاد'


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """Custom user that support email instead of username"""

    USER_ROLE = (('a', 'ادمین'), ('o', 'ناظر'), ('c', 'مشتری'))
    email = models.EmailField(verbose_name='ایمیل', max_length=255, unique=True)
    phone = models.CharField(verbose_name='شماره تلفن', max_length=11, unique=True,
                             validators=[RegexValidator(r'^09\d{9}',
                                                        message='تلفن نا معتبر',
                                                        code='invalid_phone')])
    first_name = models.CharField(verbose_name='نام', max_length=64, null=True)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=64, null=True)
    is_active = models.BooleanField(verbose_name='فعال', default=False)
    is_staff = models.BooleanField(verbose_name='کارمند', default=False)
    role = models.CharField(verbose_name='نقش کاربر', choices=USER_ROLE, max_length=1, default='c')
    profile_image = models.ImageField(verbose_name='تصویر پروفایل', upload_to=user_image_file_path, null=True, blank=True, default=f'uploads/user/no_image.png')

    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL, null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        if self.role == 'o':
            my_group = Group.objects.get(name='ناظر')
            my_group.user_set.add(self)

        if self.role == 'a':
            my_group = Group.objects.get(name='ادمین')
            my_group.user_set.add(self)
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربر ها'

    @property
    def full_name(self):
        if (f := self.first_name) and (l := self.last_name):
            return f'{f} {l}'
        return f'{self.email}'

    def jlast_login(self):
        return to_jalali(self.last_login)
    jlast_login.short_description = 'آخرین ورود'

    def display_profile_image(self):
        if self.profile_image:
            return format_html('<img width=64 src={}>'.format(self.profile_image.url))

    display_profile_image.short_description = 'تصویر'

    # def get_discounts(self):
    #     return "\n".join([d.neme for d in self.discount.all()])

    def __str__(self) -> str:
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


class DescountManager(models.Manager):
    def active(self):
        return self.filter(Q(limit__gt=0)|Q(limit=None),
                           end_date__gt=timezone.now(), 
                           start_date__lt=timezone.now()
                           )
    
    
class Discount(BaseModel):
    name = models.CharField(verbose_name='نام تخفیف', max_length=255, unique=True)
    code = models.CharField(verbose_name='کد تخفیف', unique=True, max_length=16)
    percent = models.PositiveIntegerField(verbose_name='درصد تخفیف',
                                          validators=[MinValueValidator(1), MaxValueValidator(100)],
                                          null=True, blank=True)
    mablagh = models.PositiveIntegerField(verbose_name='حداکثر مبلغ قابل تخفیف', null=True, blank=True)
    limit = models.PositiveIntegerField(verbose_name='حداکثر تعداد قابل فروش (خالی برای نامحدود)', null=True, blank=True)
    start_date = models.DateTimeField(verbose_name='تاریخ شروع')
    end_date = models.DateTimeField(verbose_name='تاریخ پایان')
    single_use = models.BooleanField(verbose_name='یکبار مصرف', default=True)
    meta_description = models.CharField(verbose_name='توضیح کوتاه (SEO)', max_length=255, null=True, blank=True)
    description = models.TextField(verbose_name='توضیحات', max_length=1000, null=True, blank=True)

    objects = DescountManager()

    def is_active(self):
        return self.end_date > timezone.now() and self.start_date < timezone.now() and (self.limit is None or self.limit > 0)
    is_active.boolean = True

    class Meta:
        verbose_name = 'تخفیف'
        verbose_name_plural = 'تخفیف ها'

        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_percent_or_mablagh",
                check=(
                    models.Q(percent__isnull=True, mablagh__isnull=False)
                    | models.Q(percent__isnull=False, mablagh__isnull=True)
                    | models.Q(percent__isnull=False, mablagh__isnull=False)
                ),
            )
        ]

    def __str__(self):
        return f'{self.code}'
