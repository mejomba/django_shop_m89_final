from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .mixins import StaffOrJwtLoginRequiredMixin

import jwt
from jwt import exceptions

# class Profile(JwtLoginRequiredMixin, generic.DetailView):
#     model = get_user_model()
#     template_name = 'core/profile.html'
#


class Profile(StaffOrJwtLoginRequiredMixin, generic.View):
    def get(self, request):
        return render(request, 'core/profile.html', {})

#
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
