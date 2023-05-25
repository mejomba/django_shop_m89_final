from django.urls import path
from . import views


app_name = 'shop'
urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('product/', views.ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('discount/', views.DiscountListView.as_view(), name='discount_list'),
    path('magicsale/', views.MagicSaleListView.as_view(), name='magic_sale_list'),
]