from typing import Any, Dict
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views import generic

from . import models


def landing_page(request):
    magicsale = models.MagicSale.objects.active()
    discounts = models.Discount.objects.active()
    categories = models.Category.objects.filter(parent_category=None)

    if discounts:
        products_list = [discount.product_discount_related_name.all().distinct() for discount in discounts]
        products = products_list[0].union(*products_list)
    else:
        products = []

    last_products = models.Product.objects.all().order_by('-create_at')[:4]
    
    context = {'magicsale': magicsale, 'products': products, 'categories': categories, 'last_products': last_products}
    return render(request, 'shop/landing_page.html', context)


class ProductListView(generic.ListView):
    model = models.Product
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
        context['comments'] = models.Comment.objects.filter(product=self.kwargs['pk']).order_by('-create_at')
        return context


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
        products = category.product_category_related_name.all()
        return products


class DiscountListView(generic.ListView):
    model = models.Discount
    template_name = 'shop/discount_page.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        discounts = models.Discount.objects.active()
        products_list = [discount.product_discount_related_name.all().distinct() for discount in discounts]
        context['products'] = products_list[0].union(*products_list)
        return context


class MagicSaleListView(generic.ListView):
    model = models.MagicSale
    template_name = 'shop/magic_sale_list.html'
    context_object_name = 'magic_sales'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        magic_sales = models.MagicSale.objects.active()
        products_list = [models.Product.objects.filter(magic_sale=magic) for magic in magic_sales]
        context['products'] = products_list[0].union(*products_list)

        return context
