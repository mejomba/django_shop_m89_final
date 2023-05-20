from django.urls import path
from . import views


app_name = 'product'
urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('product/', views.ProductListView.as_view(), name='product_list')
]