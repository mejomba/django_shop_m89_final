from django.db import models
from django.conf import settings
from django.utils import timezone

import datetime

from core.models import BaseModel, Address
from shop.models import Product


class Cart(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')

    # TODO "get total cart price base on final price of products"
    # def get_total_price(self):
    #     total = 0
    #     products = CartItem.objects.filter(cart=self)
    #     for product in products:
    #         total += product.get_final_price
    #     return total

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد خرید ها'

    def __str__(self):
        return f'{self.user}'


class CartItem(BaseModel):
    count = models.PositiveIntegerField(verbose_name='تعداد')

    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'آیتم سبد خرید'
        verbose_name_plural = 'آیتم های سبد خرید'

    def __str__(self):
        return f'{self.cart} : {self.product}'


class Order(BaseModel):
    ORDER_STATUS = (
        ('1', 'در انتظار پرداخت'),
        ('2', 'پرداخت موفق'),
        ('3', 'پرداخت ناموفق'),
        ('4', 'انصراف'),
        ('5', 'منقضی شده'),
        ('6', 'آماده ارسال'),
        ('7', 'ارسال شده'),
        ('8', 'تحویل شده'),
    )
    SHIPPING_METHOD = (
        ('1', 'ارسال پست عادی'),
        ('2', 'ارسال پست سفارشی'),
        ('3', 'ارسال پست پیشتاز'),
        ('4', 'ارسال تیپاکس'),
        ('5', 'ارسال ترمینال'),
        ('6', 'ارسال پیک'),
    )
    status = models.CharField(choices=ORDER_STATUS, max_length=1, verbose_name='وضعیت', default='1')
    shipping = models.CharField(choices=SHIPPING_METHOD, max_length=1, verbose_name='روش ارسال')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    time_for_pay = models.DateTimeField(verbose_name='زمال مجاز برای پرداخت')

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'

    def __str__(self):
        return f'{self.user} : {self.status}'

    def save(self, *args, **kwargs):
        if not self.time_for_pay:
            self.time_for_pay = timezone.now() + datetime.timedelta(minutes=30)
            self.save()
        return super().save(*args, **kwargs)

    # TODO "calculate total price of order after discount"
    # def get_order_total_price(self):
    #     pass


class OrderItem(BaseModel):
    count = models.PositiveIntegerField(verbose_name='تعداد')

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم های سفارش'

    def __str__(self):
        return f'{self.order} : {self.product}'


class Transaction(BaseModel):
    TRANSACTION_STATUS = (
        ('1', 'در انتظار'),
        ('2', 'موفق'),
        ('3', 'نا موفق'),
    )
    status = models.CharField(verbose_name='وضعیت', choices=TRANSACTION_STATUS, max_length=1)
    transaction_code = models.CharField(verbose_name='کد تراکنش', max_length=64)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(verbose_name='قیمت کل')

    class Meta:
        verbose_name = 'تراکنش'
        verbose_name_plural = 'تراکنش ها'

    def __str__(self):
        return f'{self.user.email} : {self.transaction_code}'
