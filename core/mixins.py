from django.utils.text import gettext_lazy as _
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
import jwt
from jwt import exceptions

from django.http import HttpResponseRedirect, Http404

from config import settings
from order.models import Cart, Order

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class AuthenticatedAccessDeniedMixin:
    def dispatch(self, request, *args, **kwargs):
        PROFILE_URL = reverse('core:profile')
        LANDINGPAGE_URL = reverse('shop:landing_page')

        if request.user.is_staff or request.user.is_superuser:
            return redirect(PROFILE_URL)

        if token := request.COOKIES.get('jwt'):
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user = get_user_model().objects.filter(id=payload.get('id')).first() or \
                       get_user_model().objects.filter(id=payload.get('user_id')).first()
                if user and user.is_active:
                    request.user = user
                    return redirect(PROFILE_URL)
                if user and not user.is_active:
                    messages.warning(request, _('حساب شما ایجاد شده اما هنوز فعال نشده، از ایمیل فعال سازی استفاده کنید'))
                    return redirect(LANDINGPAGE_URL)
            except Exception:
                pass
        return super().dispatch(request, *args, **kwargs)


class StaffOrJwtLoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        LOGIN = reverse('core:login_view')
        response = HttpResponseRedirect(LOGIN)
        if request.user and (request.user.is_superuser or request.user.is_staff):
            return super().dispatch(request, *args, **kwargs)
        if token := request.COOKIES.get('jwt'):
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user = get_user_model().objects.filter(id=payload.get('id')).first() or \
                       get_user_model().objects.filter(id=payload.get('user_id')).first()
                if not user:
                    messages.error(request, _('برای استفاده از این صفحه ابتدا وارد شوید.'))
                    response.status_code = 401
                    return response

                if not user.is_active:
                    messages.info(request, _('حساب کاربری شما ایجاد شده اما فعال نشده، یک ایمیل فعال ساری برای شما ارسال کردیم روی ایمیل فعال سازی کلیک کنید.'))
                    return redirect('shop:landing_page')
                request.user = user
                return super().dispatch(request, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                messages.error(request, _('اعتبار توکن احراز هویت شما به پایان رسیده است. دوباره وارد شوید.'))
                return redirect(LOGIN)
            except exceptions.InvalidTokenError:
                messages.error(request, _('توکن ارسال شده معتبر نمیباشد. دوباره وارد شوید.'))
                return redirect(LOGIN)
        else:
            messages.error(request, _('برای استفاده از این صفحه باید وارد شوید.'))
            return redirect(LOGIN)


class JWTRequiredForAuthenticateMixin:
    def dispatch(self, request, *args, **kwargs):
        LOGIN_URL = reverse('core_api:login')
        PROFILE_URL = reverse('core:profile')

        if token := request.COOKIES.get('jwt'):
            response = HttpResponseRedirect(LOGIN_URL)
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user = get_user_model().objects.filter(id=payload.get('id')).first() or \
                       get_user_model().objects.filter(id=payload.get('user_id')).first()
                if not user:
                    response.delete_cookie('jwt')
                    return response

                request.user = user
                response = HttpResponseRedirect(PROFILE_URL)
                return response

            except jwt.ExpiredSignatureError:
                response.delete_cookie('jwt')
                messages.error(request, _('اعتبار توکن احراز هویت شما به پایان رسیده است. دوباره وارد شوید.'))
                return response
            except exceptions.InvalidTokenError:
                messages.error(request, _('توکن ارسال شده معتبر نمیباشد. دوباره وارد شوید.'))
                response.delete_cookie('jwt')
                return response
        else:
            response = HttpResponseRedirect(LOGIN_URL)
            # response = HttpResponseRedirect(PROFILE_URL)
            return render(request, 'core/login.html', {})
            # return response


class CartAuthorMixin:
    def dispatch(self, request, pk, *args, **kwargs):
        cart = get_object_or_404(Cart, pk=pk)
        print("cart author mixin ===", cart.user)
        if request.user == cart.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404


class ProfileAuthorMixin:
    def dispatch(self, request, pk, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=pk)
        print(request.user, " ==== profile author mixin === ", user)
        if request.user == user:
            return super().dispatch(request, pk, *args, **kwargs)
        else:
            raise Http404
            # return HttpResponse('user not found', status=404)


class OrderAuthorMixin:
    def dispatch(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk)
        print(request.user, " ==== profile author mixin === ", order.user)
        if request.user == order.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404
            # return HttpResponse('user not found', status=404)

