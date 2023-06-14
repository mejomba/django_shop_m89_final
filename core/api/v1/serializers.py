from django.contrib.auth import get_user_model
from rest_framework import serializers
from ... import models

import re

from .exception import PasswordValidation
from ...models import user_image_file_path


class LoginVerificationSerializer(serializers.Serializer):
    jwt = serializers.CharField()


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
    profile_image = serializers.ImageField(required=False)

    def validate_profile_image(self, image):
        # 2MB
        MAX_FILE_SIZE = 2000000
        if image.size > MAX_FILE_SIZE:
            print(image.size)
            raise serializers.ValidationError("File size too big!")
        return image

    class Meta:
        model = get_user_model()
        exclude = ['password', 'is_active', 'is_deleted', 'delete_date']
        # exclude = ['password']


class UserUpdateSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False)

    def validate_profile_image(self, image):
        # 2MB
        MAX_FILE_SIZE = 2000000
        if image.size > MAX_FILE_SIZE:
            print(image.size)
            raise serializers.ValidationError("File size too big!")
        return image

    class Meta:
        model = get_user_model()
        exclude = ['password', 'is_active', 'is_staff', 'is_superuser', 'is_deleted', 'delete_date', 'role']
        # fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'profile_image']