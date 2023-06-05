from django.utils import timezone
from typing import Any, Dict
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect, reverse
from django.views import generic
from django.contrib import messages
from django.db.models import Prefetch

from core import utils
from . import models
from .forms import CommentForm


def landing_page(request):
    magicsale = models.MagicSale.objects.active()
    discounts = models.Discount.objects.active()
    categories = models.Category.objects.filter(parent_category=None)

    if discounts:
        products_list = [discount.product_discount_related_name.filter(quantity__gt=0).distinct() for discount in discounts]
        products = products_list[0].union(*products_list)
    else:
        products = []

    last_products = models.Product.objects.filter(quantity__gt=0).order_by('-create_at')[:4]
    
    context = {'magicsale': magicsale, 'products': products, 'categories': categories, 'last_products': last_products}
    return render(request, 'shop/landing_page.html', context)


class ProductListView(generic.ListView):
    model = models.Product
    queryset = models.Product.objects.filter(quantity__gt=0)
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # context['images'] = models.ProductImage.objects.filter(product=self.kwargs['pk'])
        # context['comments'] = models.Comment.objects.filter(product=self.kwargs['pk']).order_by('-create_at')
        print(context)
        return context


class ProductDetailView(generic.DetailView):
    model = models.Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['images'] = models.ProductImage.objects.filter(product=self.kwargs['pk'])
        context['comments'] = models.Comment.objects.filter(product=self.kwargs['pk'], is_deleted=False).order_by('-create_at')
        context['form'] = CommentForm()
        print(context)
        return context

    def post(self, request, pk):
        form = CommentForm(request.POST)
        if form.is_valid():
            product = models.Product.objects.filter(pk=pk).first()
            parent_comment = models.Comment.objects.filter(pk=form.cleaned_data['parent_comment']).first()
            models.Comment.objects.create(content=form.cleaned_data['content'],
                                          rating=form.cleaned_data['rating'],
                                          parent_comment=parent_comment,
                                          product=product,
                                          user=request.user)
        else:
            print('form invalid')
        return redirect(reverse('shop:product_detail', kwargs={'pk': pk}))


def remove_comment(request, pk):
    if request.method == 'POST':
        comment = models.Comment.objects.filter(pk=pk).first()
        print(comment.user)
        if comment and request.user == comment.user:
            comment.is_deleted = True
            comment.delete_date = timezone.now()
            comment.save()
            utils.remove_related_object(comment)
            # for sub_comment in comment.related_name.all():
            #     pass
            # comment.delete()
            messages.success(request, 'کامنت با موفقیت حذف شد')
    return redirect(request.META.get('HTTP_REFERER'))


class CategoryListView(generic.ListView):
    model = models.Category
    template_name = 'shop/category_list.html'
    context_object_name = 'categories'
    

class CategoryDetailView(generic.ListView):
    template_name = 'shop/category_detail.html'
    context_object_name = 'products'
    paginate_by = 2
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(models.Category, id=self.kwargs['pk'])
        return context

    def get_queryset(self):
        category = get_object_or_404(models.Category, pk=self.kwargs['pk'])
        products = category.product_category_related_name.filter(quantity__gt=0)
        return products


class DiscountListView(generic.ListView):
    model = models.Discount
    template_name = 'shop/discount_page.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        discounts = models.Discount.objects.active()
        products_list = [discount.product_discount_related_name.filter(quantity__gt=0).distinct() for discount in discounts]
        context['products'] = products_list[0].union(*products_list)
        return context


class MagicSaleListView(generic.ListView):
    model = models.MagicSale
    template_name = 'shop/magic_sale_list.html'
    context_object_name = 'magic_sales'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        magic_sales = models.MagicSale.objects.active()
        products_list = [models.Product.objects.filter(magic_sale=magic, quantity__gt=0) for magic in magic_sales]
        context['products'] = products_list[0].union(*products_list)

        return context
