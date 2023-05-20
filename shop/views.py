from django.shortcuts import render
from django.views import generic

from . import models


def landing_page(request):
    return render(request, 'shop/landing_page.html', {})
    # return render(request, 'core/register.html', {})
    # return render(request, 'core/login.html', {})
    # return render(request, 'core/profile.html', {})
    # return render(request, 'core/order_history.html', {}) # load in profile first view
    # return render(request, 'core/address.html', {})
    # return render(request, 'shop/discount_page.html', {})
    # return render(request, 'shop/product_list.html', {})


class ProductListView(generic.ListView):
    model = models.Product
    template_name = 'product_list.html'
    context_object_name = 'products'
