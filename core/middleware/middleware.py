import jwt
from jwt import exceptions

from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import redirect


class JWTAuthenticateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if token := request.COOKIES.get('jwt'):
            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                user = get_user_model().objects.filter(id=payload['id']).first()
                if user and user.is_active:
                    request.user = user
            except Exception:
                pass

        response = self.get_response(request)

        return response
