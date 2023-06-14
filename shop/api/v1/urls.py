from django.urls import path
from . import views

app_name = 'shop_api'

urlpatterns = [
    # path('v1/cart/', views.CartAPI.as_view(), name='cart'),
    path('v1/cart/<int:pk>/', views.CartItemAPI.as_view(), name='cart'),
    path('v1/cart/', views.CartAPI.as_view(), name='cart2'),
    # path('v1/cart/submit/', views.CartAPI.as_view(), name='cart_to_order'),
    path('v1/order/<int:pk>/', views.OrderAPI.as_view(), name='order_api'),
    path('v1/order/create/', views.CreateOrderAPI.as_view(), name='create_order_api'),
    path('v1/order/', views.OrderListAPI.as_view(), name='order_list_api'),
    path('v1/payment/', views.Payment.as_view(), name='payment'),
    path('v1/cart/discount/', views.DiscountAPI.as_view(), name='discount')
    # path('cart/add/<int:pk>/', views.AddToCartAPI.as_view(), name='add_to_cart'),
    # path('cart/delete/<int:pk>/', views.DeleteFromCartAPI.as_view(), name='delete_from_cart'),
]