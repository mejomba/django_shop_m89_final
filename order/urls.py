from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    # path('cart/<int:pk>/', views.CartView.as_view(), name='cart2'),
    path('cart/<int:pk>/', views.CartView.as_view(), name='cart2'),
    path('payment/bank/', views.bank, name='bank'),
]