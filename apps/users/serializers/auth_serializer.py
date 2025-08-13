import logging

from typing import Dict, Any
from django.db import transaction
from django.conf import settings
from rest_framework import serializers
from apps.users.backend import CustomAuthBackend
from apps.users.models import User


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if self.instance:
            if 'email' in data and self.instance.email != data['email']:
                if User.objects.filter(email=data['email']).exists():
                    raise serializers.ValidationError("A user with this email already exists.")
        else:
            if 'email' in data and User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError("A user with this email already exists.")

        return data

    def create(self, validated_data: Dict[str, Any]) -> 'User':
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.save()
        return user

    def update(self, instance: 'User', validated_data: Dict[str, Any]):
        with transaction.atomic():
            instance.email = validated_data.get('email', instance.email)
            if 'password' in validated_data:
                instance.set_password(validated_data['password'])
            instance.save()
            profile = instance.profile
            profile.save()
        return instance


class AuthenticationSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data['email']
        password = data['password']

        user = CustomAuthBackend().authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials.")

        self.context['user'] = user
        return data

    def to_representation(self, instance):
        user = self.context['user']
        data = {
            'email': user.email,
            'user_id': user.id,
            'token': user.token(secret_key=settings.JWT_TOKEN),
            'refresh_token': user.refresh_token(secret_key=settings.JWT_TOKEN),
        }
        return data
