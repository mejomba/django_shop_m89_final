from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # path('profile/<int:pk>/', views.Profile.as_view(), name='profile'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('jwt/admin/logout/', views.admin_logout, name='admin_logout'),
    path('register/', views.Register.as_view(), name='register_view'),
    path('login/', views.LoginView.as_view(), name='login_view'),
    path('search/', views.search, name='search'),
]
