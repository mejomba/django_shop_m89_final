from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer


class RegisterUserAPI(APIView):
    def post(self, request):
        serializer_ = UserSerializer(data=request.data)
        serializer_.is_valid(raise_exception=True)
        serializer_.save()
        return Response(serializer_.data, status=status.HTTP_201_CREATED)
    
