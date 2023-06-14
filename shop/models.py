import uuid
import os

from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify

from core.models import BaseModel, Discount
from core.models_on_delete import SOFT_CASCADE


def post_image_file_path(instance, filename: str):
    """generate file path for user profile image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join(f'uploads/post/{timezone.now().date()}', filename)


def discount_solver(product_instance):
    sum_mablagh = 0
    sum_percent = 0
    categories = product_instance.category.all()

    all_discounts = [c.discount.all() for c in categories]
    all_discounts.append(product_instance.discount.all())

    for queryset in all_discounts:
        for discount in queryset:
            limit = discount.limit
            if limit is None or limit > 0:
                if (p := discount.percent) and (m := discount.mablagh):
                    if product_instance.price * (p / 100) > m:
                        sum_mablagh += m
                    else:
                        sum_percent += p
                elif p := discount.percent:
                    sum_percent += p
                elif m := discount.mablagh:
                    sum_mablagh += m

    return sum_mablagh, sum_percent


class CategoryManager(models.Manager):
    def menu(self):
        return self.filter(show_in_menu=True)
    
    
class Category(BaseModel):
    title = models.CharField(verbose_name='عنوان دسته', max_length=64)
    meta_title = models.CharField(verbose_name='عنوان دسته(SEO)', max_length=64, null=True, blank=True)
    meta_description = models.CharField(verbose_name='توضیح کوتاه', max_length=255, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    show_in_menu = models.BooleanField(default=False)

    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    discount = models.ManyToManyField(Discount, related_name='category_discount_related_name', null=True, blank=True)

    objects = CategoryManager()
    
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return f'{self.title}'


class Product(BaseModel):
    name = models.CharField(verbose_name='نام محصول', max_length=255)
    brand = models.CharField(verbose_name='سازنده', max_length=128)
    price = models.PositiveIntegerField(verbose_name='قیمت')
    quantity = models.PositiveIntegerField(verbose_name='تعداد موجودی')
    tax = models.FloatField(verbose_name='درصد مالیات', default=9, validators=[MinValueValidator(0), MaxValueValidator(100)])
    slug = models.SlugField(verbose_name='نام منحصر به فرد', max_length=100, unique=True)
    meta_description = models.CharField(verbose_name='توضیح کوتاه', max_length=255)
    description = models.TextField(verbose_name='توضیح کامل', max_length=5000, null=True, blank=True)
    extra_data = models.JSONField(verbose_name='مشخصات اضافه(JSON)', null=True, blank=True)
    thumbnail = models.ImageField(verbose_name='تصویر اصلی', upload_to=post_image_file_path)

    discount = models.ManyToManyField(Discount, related_name='product_discount_related_name', null=True, blank=True, verbose_name='تخفیف')
    category = models.ManyToManyField('Category', related_name='product_category_related_name',verbose_name='دسته بندی')
    tag = models.ManyToManyField('Tag', related_name='product_category_related_name')
    magic_sale = models.ForeignKey('MagicSale', on_delete=models.SET_NULL, verbose_name='حراج شگفت انگیز', null=True, blank=True, default=None)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصول ها'

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_final_price(self):
        return self.get_price_apply_tax()
    get_final_price.short_description = 'قیمت نهایی'
    
    def get_price_apply_tax(self):
        price = self.get_price_apply_discount()
        return int(price + (price * (self.tax / 100)))
        # return int(price * (self.tax / 100))
    get_price_apply_tax.short_description = 'قیمت پس از مالیات'

    def tax_value(self):
        price = self.price
        return int(price * (self.tax / 100))

    def get_price_apply_discount(self):
        price = self.price
        sum_mablagh, sum_percent = discount_solver(self)

        if sum_mablagh >= price or sum_percent >= 100:
            return 0

        price -= (price * (sum_percent/100))
        price -= sum_mablagh

        if price <= 0:
            return 0

        return int(price)
    get_price_apply_discount.short_description = 'قیمت پس از تخفیف'

    def __str__(self):
        return f'{self.name}'


class ProductImage(BaseModel):
    image = models.FileField(verbose_name='تصویر', upload_to=post_image_file_path)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'تصویر محصول'
        verbose_name_plural = 'تصویر های گالری محصول'

    def __str__(self):
        return f'{self.product.name}'


class WishList(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'لیست علاق مندی'
        verbose_name_plural = 'لیست علاقه مندی ها'

    def __str__(self):
        return f'{self.user.full_name}'


class Tag(BaseModel):
    name = models.CharField(verbose_name='تگ', max_length=32)

    class Meta:
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ ها'

    def __str__(self):
        return f'{self.name}'


class Comment(BaseModel):
    content = models.TextField(verbose_name='متن نظر', max_length=500)
    rating = models.PositiveIntegerField(verbose_name='امتیاز', validators=[MinValueValidator(1), MaxValueValidator(5)])

    parent_comment = models.ForeignKey('self', on_delete=SOFT_CASCADE, null=True, blank=True, related_name='related_name')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظر ها'

    def __str__(self):
        return f'{self.content}'


class MagicSaleManager(models.Manager):
    def active(self):
        return self.filter(end_date__gt=timezone.now(), start_date__lt=timezone.now())
    
    
class MagicSale(BaseModel):
    name = models.CharField(verbose_name='نام', max_length=255)
    slug = models.SlugField(verbose_name='نام منحصر به فرد', max_length=100, unique=True)
    start_date = models.DateTimeField(verbose_name='تاریخ شروع')
    end_date = models.DateTimeField(verbose_name='تاریخ پایان')

    objects = MagicSaleManager()
    
    class Meta:
        verbose_name = 'حراج شگفت انگیز'
        verbose_name_plural = 'حراج های شگفت انگیز'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            self.save()
        return super().save(*args, **kwargs)

