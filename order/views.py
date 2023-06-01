from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404
from .models import Cart, Order, OrderItem
from core.mixins import StaffOrJwtLoginRequiredMixin, CartAuthorMixin


class CartView(CartAuthorMixin, generic.DetailView):
    model = Cart
    context_object_name = 'cart'
    template_name = 'order/cart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def bank(request):
    return render(request, 'order/bank.html', {})
# def cart_to_order(request, pk):
#     if request.method == 'POST':
#         cart = get_object_or_404(Cart, pk=pk)
#         cart_item = cart.cartitem_set.filter(is_deleted=False)
#         for item in cart_item:
#             # OrderItem.objects.create()
#             print("==========", item, "====", item.count)
#     context = {'cart': cart}
#     return render(request, 'order/cart.html', context)
