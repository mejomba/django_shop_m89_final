from django.utils import timezone

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import get_user_model, login, logout
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.contrib import messages

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.authentication import TokenAuthentication
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from core.utils import send_confirmation_email

import jwt, datetime
from core.mixins import AuthenticatedAccessDeniedMixin

from .serializers import UserSerializer, UserLoginSerializer, UserRegisterSerializer


class RegisterUserAPI(AuthenticatedAccessDeniedMixin, APIView):

    def get(self, request):
        return render(request, 'core/register.html', {})

    def post(self, request):
        # return Response({'key': 'val'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_ = UserRegisterSerializer(data=request.data)
        serializer_.is_valid(raise_exception=True)
        serializer_.save()
        request.email = serializer_.validated_data['email']
        # TODO use celery for send email
        send_confirmation_email(request, serializer_.data['id'])
        return Response(serializer_.data, status=status.HTTP_201_CREATED)

        # print('exception ===========')
        # response = Response()
        #
        # return Response(serializer_.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(AuthenticatedAccessDeniedMixin, APIView):
    # authentication_classes = [TokenAuthentication]
    def get(self, request):
        # print(request.user)
        # PROFILE_URL = reverse('core:profile')
        #
        # if request.user.is_staff or request.user.is_superuser:
        #     return redirect(PROFILE_URL)
        #
        # if token := request.COOKIES.get('jwt'):
        #     try:
        #         payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        #         user = get_user_model().objects.filter(id=payload['id']).first()
        #         if user:
        #             request.user = user
        #             return redirect(PROFILE_URL)
        #     except Exception:
        #         return render(request, 'core/login.html', {})
        #     # return redirect(PROFILE_URL)

        return render(request, 'core/login.html', {})

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = get_user_model().objects.filter(email=email).first()

        if user is None:
            # messages.error(request, 'کاربر با این اطلاعات یافت نشد.')
            # raise AuthenticationFailed('user not found')
            return Response({'detail': 'کاربر با این مشخصات یافت نشد'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            # messages.error(request, 'رمز عبور اشتباه است')
            # raise AuthenticationFailed('incorrect password')
            return Response({'detail': 'رمز عبور اشتباه'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({'detail': 'حساب کاربری شما فعال نیست'}, status=status.HTTP_401_UNAUTHORIZED)

        user.last_login = timezone.now()
        user.save()

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=10),
            'iat': datetime.datetime.utcnow()
        }

        # token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        # login(request, user)  # login with django for django login required views
        response.data = {
            'jwt': token
        }
        return response


class LogoutAPI(APIView):
    def post(self, request):
        # response = Response()
        landing_page = reverse('shop:landing_page')
        response = HttpResponseRedirect(landing_page)
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success',
        }

        if request.user.is_staff:
            logout(request)  # logout staff user

        return response
        # return redirect('shop:landing_page')
        # landing_page = reverse('shop:landing_page')
        # return HttpResponseRedirect(redirect_to=landing_page)


# class Profile(APIView):
#     def get(self, request):
#         token = request.COOKIES.get('token')
#         context = {}
#
#         if not token:
#             return render(request, 'core/login.html', context)
#
#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             return render(request, 'core/login.html', context)
#         except Exception:
#             return Http404
#
#         user = get_user_model().objects.filter(id=payload['id']).first()
#         serializer_ = UserSerializer(user)
#         context = {'user': serializer_.data}
#         return render(request, 'core/profile.html', context)
#         # return Response(serializer_.data)

