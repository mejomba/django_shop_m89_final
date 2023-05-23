from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('v1/register/', views.RegisterUserAPI.as_view(), name='register'),
    path('v1/login/', TokenObtainPairView.as_view(), name='login'),
    path('v1/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]