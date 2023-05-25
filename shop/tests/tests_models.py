from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.utils import timezone
import datetime
from django.utils.text import slugify

from shop.models import Category, Product, MagicSale, Comment


class CategoryModelTest(TestCase):
    def setUp(self) -> None:
        self.test_parent = Category('title', 'meta title', 'meta description', 'description')
        self.test_category = Category('title', 'meta title', 'meta description', 'description', parent_category=self.test_parent)

    def test_category_str(self):
        category = self.test_category
        self.assertEqual(str(category), f'{category.title}')

    def test_parent_category(self):
        self.assertEqual(self.test_category.parent_category, self.test_parent)


class ProductModelTest(TestCase):
    def setUp(self) -> None:
        self.test_product = Product('name', 'brand', 1234, 1234)


    def test_product_slug(self):
        slug = slugify(self.test_product.name)
        self.assertEqual(self.test_product.slug, slug)

    def test_product_str(self):
        self.assertEqual(str(self.test_product), self.test_product.name)


class CommentModelTest(TestCase):
    def setUp(self) -> None:
        self.test_user = get_user_model().objects.create(email='mail@mail.com', password='Test1234')
        self.test_product = Product('name', 'brand', 1234, 1234)
        self.test_parent = Comment('content', 3, None, self.test_product, self.test_user)
        self.test_comment = Comment('content', 5, parent_comment=self.test_parent, product=self.test_product, user=self.test_user)

    def test_comment_str(self):
        comment = self.test_comment
        self.assertEqual(str(comment), f'{comment.content}')

    def test_parent_category(self):
        self.assertEqual(self.test_comment.parent_comment, self.test_parent)


class MagicSaleModelTest(TestCase):
    def setUp(self) -> None:
        self.test_magic_sale = MagicSale('name')

    def test_magi_sale_slug(self):
        slug = slugify(self.test_magic_sale.name)
        self.assertEqual(self.test_magic_sale.slug, slug)

    def test_magic_sale_str(self):
        self.assertEqual(str(self.test_magic_sale), self.test_magic_sale.name)
