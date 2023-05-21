from typing import Any, Dict
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views import generic

from . import models


def landing_page(request):
    # return render(request, 'shop/landing_page.html', {})
    # return render(request, 'core/register.html', {})
    # return render(request, 'core/login.html', {})
    return render(request, 'core/profile.html', {})
    # return render(request, 'core/order_history.html', {}) # load in profile first view
    # return render(request, 'core/address.html', {})
    # return render(request, 'shop/discount_page.html', {})
    # return render(request, 'shop/product_list.html', {})


class ProductListView(generic.ListView):
    model = models.Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'


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
    

class CategoryDetailView(generic.DetailView):
    model = models.Category
    template_name = 'shop/category_detail.html'
    context_object_name = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(models.Category, pk=self.kwargs['pk'])
        context["products"] = category.product_category_related_name.all()
        return context
    