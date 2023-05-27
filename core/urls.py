from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # path('profile/<int:pk>/', views.Profile.as_view(), name='profile'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('<str:uidb64>/<str:token>', views.activate, name='activate')
]
