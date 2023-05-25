from django.urls import path
from . import views
import core
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'core_api'

urlpatterns = [
    path('v1/register/', views.RegisterUserAPI.as_view(), name='register'),
    # path('v1/login/', TokenObtainPairView.as_view(), name='login'),
    path('v1/login/', views.LoginAPI.as_view(), name='login'),
    path('v1/logout/', views.LogoutAPI.as_view(), name='logout'),
    path('v1/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('v1/profile/', views.Profile.as_view(), name='profile'),

]