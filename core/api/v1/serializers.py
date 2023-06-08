from django.contrib.auth import get_user_model
from rest_framework import serializers
from ... import models

import re

from .exception import PasswordValidation


class UserRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'phone', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }
        
    def create(self, validated_data):
        password_pattern = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        if not re.match(password_pattern, validated_data['password']):
            raise PasswordValidation

        user = self.Meta.model.objects.create(email=validated_data['email'],
                                              phone=validated_data['phone'],
                                              first_name=validated_data['first_name'],
                                              last_name=validated_data['last_name'],
                                              )

        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ['password']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'first_name', 'last_name', 'phone']