from django.utils import timezone

from django.contrib.auth import get_user_model, login, logout
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.contrib import messages
from django.core.cache import cache
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response

from core.utils import send_confirmation_email

import jwt, datetime
from core.mixins import AuthenticatedAccessDeniedMixin, JWTRequiredForAuthenticateMixin, StaffOrJwtLoginRequiredMixin, \
    ProfileAuthorMixin

from .serializers import UserSerializer, UserLoginSerializer, UserRegisterSerializer, UserUpdateSerializer

from core import utils


class RegisterUserAPI(AuthenticatedAccessDeniedMixin, APIView):

    # def get(self, request):
    #     return render(request, 'core/register.html', {})

    def post(self, request):
        serializer_ = UserRegisterSerializer(data=request.data)
        serializer_.is_valid(raise_exception=True)
        serializer_.save()
        request.email = serializer_.validated_data['email']
        # TODO use celery for send email
        send_confirmation_email(request, serializer_.data['id'])
        return Response(serializer_.data, status=status.HTTP_201_CREATED)


class LoginAPI(AuthenticatedAccessDeniedMixin, APIView):
    def get(self, request):
        return render(request, 'core/login.html', {})

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        auth_type = request.POST.get('auth_type')

        user = get_user_model().objects.filter(email=email).first()

        if user is None:
            return Response({'detail': 'کاربر با این مشخصات یافت نشد'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({'detail': 'رمز عبور اشتباه'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({'detail': 'حساب کاربری شما فعال نیست'}, status=status.HTTP_401_UNAUTHORIZED)

        # generate OTP code and send to user
        utils.perform_2step_verification(user, auth_type)
        return Response({'detail': 'در انتظار تایید کد ارسال شده'}, status.HTTP_200_OK)


class LoginVerification(AuthenticatedAccessDeniedMixin, APIView):
    def get(self, request):
        return render(request, 'core/login.html', {})

    def post(self, request):
        print('================', request.META.get('HTTP_REFERER'))
        otp_code = request.POST.get('otp_code')
        user_id = cache.get(otp_code)
        if not user_id:
            return Response({'detail': 'کد وارد شده اشتباه است یا منقضی شده'}, status.HTTP_401_UNAUTHORIZED)

        user = get_user_model().objects.filter(pk=user_id).first()
        if user:
            user.last_login = timezone.now()
            user.save()

            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=10),
                'iat': datetime.datetime.utcnow()
            }

            token = jwt.encode(payload, 'secret', algorithm='HS256')

            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {
                'jwt': token
            }
            return response
        return Response({'detail': "خطای ناشناخته"}, status.HTTP_401_UNAUTHORIZED)


class LogoutAPI(APIView):
    def post(self, request):
        landing_page = reverse('shop:landing_page')
        response = HttpResponseRedirect(landing_page)
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success',
        }

        if request.user.is_staff:
            logout(request)  # logout staff user

        return response


class EditProfileAPI(ProfileAuthorMixin, APIView):

    def get(self, request):
        serializer_ = UserSerializer(instance=request.user)
        return Response(serializer_.data)

    def patch(self, request):
        user = request.user
        serializer_ = UserUpdateSerializer(user, data=request.data)
        serializer_.is_valid(raise_exception=True)
        serializer_.save()
        return Response(serializer_.data)
