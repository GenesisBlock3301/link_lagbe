import logging

from typing import Dict, Any
from django.db import transaction
from django.conf import settings
from rest_framework import serializers

from apps.common.exceptions import UserAlreadyExists
from apps.users.backend import CustomAuthBackend
from apps.users.models import User, Profile
from apps.users.tasks import send_verification_email_task
from apps.links.serializers import UserLinkSerializer

logger = logging.getLogger(__name__)


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if self.instance:
            if 'email' in data and self.instance.email != data['email']:
                if User.objects.filter(email=data['email']).exists():
                    logger.info(f"User with email {data['email']} already exists.")
                    raise UserAlreadyExists()
        else:
            if 'email' in data and User.objects.filter(email=data['email']).exists():
                logger.info(f"User with email {data['email']} already exists.")
                raise UserAlreadyExists()

        return data

    def create(self, validated_data: Dict[str, Any]) -> 'User':
        request = self.context.get('request')
        domain = request.get_host()

        with transaction.atomic():
            user = User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                is_active=False,
            )
            user.save()
            try:
                send_verification_email_task(user.id, domain)  # call a sync function here
            except Exception as e:
                raise serializers.ValidationError("Failed to send verification email")  # rollback transaction

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
            logger.info(f"Invalid credentials for user with email {email}.")
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


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender']


class UserMeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    links = UserLinkSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'is_premium', 'is_active', 'profile', 'links']
