

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth import login, get_user_model
from django.contrib import messages
import jwt
from jwt import exceptions

from rest_framework.response import Response
from django.http import HttpResponseRedirect


# class SuperUserOrStaffMixin(AccessMixin):
#     def dispatch(self, request, *args, **kwargs):
#         print(request.user, request.user.is_superuser , request.user.is_staff)
#         if request.user and (request.user.is_superuser or request.user.is_staff):
#             return super().dispatch(request, *args, **kwargs)
#         messages.error(request, 'برای استفاده از این صفحه ابتدا وارد شوید.')
#         return redirect('core_api:login')


class StaffOrJwtLoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user and (request.user.is_superuser or request.user.is_staff):
            return super().dispatch(request, *args, **kwargs)
        if token := request.COOKIES.get('jwt'):
            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                user = get_user_model().objects.filter(id=payload['id']).first()
                if not user:
                    messages.error(request, 'برای استفاده از این صفحه ابتدا وارد شوید.')
                    return redirect('core_api:login')

                if not user.is_active:
                    messages.info(request, 'حساب کاربری شما ایجاد شده اما فعال نشده، یک ایمیل فعال ساری برای شما ارسال کردیم روی ایمیل فعال سازی کلیک کنید.')
                    return redirect('shop:landing_page')
                request.user = user
                return super().dispatch(request, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                messages.error(request, 'اعتبار توکن احراز هویت شما به پایان رسیده است. دوباره وارد شوید.')
                return redirect('core_api:login')
            except exceptions.InvalidTokenError:
                messages.error(request, 'توکن ارسال شده معتبر نمیباشد. دوباره وارد شوید.')
                return redirect('core_api:login')
        else:
            messages.error(request, 'برای استفاده از این صفحه باید وارد شوید.')
            return redirect('core_api:login')


class JWTRequiredForAuthenticateMixin:
    def dispatch(self, request, *args, **kwargs):
        LOGIN_URL = reverse('core_api:login')
        PROFILE_URL = reverse('core:profile')

        if token := request.COOKIES.get('jwt'):
            response = HttpResponseRedirect(LOGIN_URL)
            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                user = get_user_model().objects.filter(id=payload['id']).first()
                if not user:
                    response.delete_cookie('jwt')
                    return response

                request.user = user
                response = HttpResponseRedirect(PROFILE_URL)
                return response
                # return super().dispatch(request, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                response.delete_cookie('jwt')
                messages.error(request, 'اعتبار توکن احراز هویت شما به پایان رسیده است. دوباره وارد شوید.')
                return response
            except exceptions.InvalidTokenError:
                messages.error(request, 'توکن ارسال شده معتبر نمیباشد. دوباره وارد شوید.')
                response.delete_cookie('jwt')
                return response
        else:
            response = HttpResponseRedirect(LOGIN_URL)
            # response = HttpResponseRedirect(PROFILE_URL)
            return render(request, 'core/login.html', {})
            # return response

