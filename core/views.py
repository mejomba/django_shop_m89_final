from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.shortcuts import reverse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .mixins import StaffOrJwtLoginRequiredMixin


from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib import messages
from django.utils.text import gettext_lazy as _
from django.shortcuts import redirect

from .utils import account_activation_token


class Profile(StaffOrJwtLoginRequiredMixin, generic.View):
    def get(self, request):
        return render(request, 'core/profile.html', {})


# class Profile(UserPassesTestMixin, generic.View):
#     def get(self, request):
#         context = {'uuu': request.user}
#         return render(request, 'core/profile.html', context)
#
#     def test_func(self):
#         if token := self.request.COOKIES.get('jwt'):
#             try:
#                 payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#                 user = get_user_model().objects.filter(id=payload['id']).first()
#                 if not user:
#                     return False
#                 if not user.is_active:
#                     return False
#                 return True
#             except jwt.ExpiredSignatureError:
#                 return False
#             except exceptions.InvalidTokenError:
#                 return False
#         else:
#             return False


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, _('حساب شما با موفقیت فعال شد اکنون میتوانید وارد شوید'))
        return redirect('core_api:login')
    else:
        messages.error(request, _('لینک فعال سازی منقضی شده مجدد درخواست لینک فعال سازی بدهید'))
        return redirect('shop:landing_page')


def admin_logout(request):
    print('admin logout ==========')
    if request.user.is_staff:
        HOME_URL = reverse('shop:landing_page')
        logout(request)
        response = HttpResponseRedirect(HOME_URL)
        response.delete_cookie('jwt')
        return response


class Register(generic.View):
    def get(self, request):
        return render(request, 'core/register.html', {})


class LoginView(generic.View):
    def get(self, request):
        return render(request, 'core/login.html', {})