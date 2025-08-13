import jwt
import datetime
from typing import Dict, Any
from django.db import models
from django.db import transaction
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime, timedelta
from apps.users.helpers import TokenConstants, UserGenderChoices
from apps.common.models import BaseModel


class UserManager(BaseUserManager):

    def create_user(self, kw: Dict[str, Any]) -> 'User':
        if not kw.get('email', None):
            raise TypeError('User must have an email.')
        with transaction.atomic():
            user = self.model(email=kw.get('email', None))
            user.set_password(kw.get('password', None))
            user.save()
            Profile.objects.create(
                user=user
            )
        return user

    def create_superuser(self, email: str, password: str) -> 'User':
        if not email:
            raise ValueError('Email must be specified!')

        user = self.model(
            email=self.normalize_email(email)
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, BaseModel):
    email = models.EmailField(db_index=True, unique=True, max_length=150)
    password = models.CharField(max_length=128)
    is_email_verified = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self) -> str:
        return self.email or str(self.id)

    def token(self, secret_key: str, remember_me: bool = False) -> str:
        if remember_me:
            exp_minutes = TokenConstants.access_token_expiry(remember_me)
        else:
            exp_minutes = TokenConstants.access_token_expiry()
        return self._generate_jwt_token(secret_key=secret_key, exp_minutes=exp_minutes)

    # Generate Refresh Token
    def refresh_token(self, secret_key: str, remember_me: bool = False) -> str:
        if remember_me:
            exp_days = TokenConstants.refresh_token_expiry(remember_me)
        else:
            exp_days = TokenConstants.refresh_token_expiry()

        return self._generate_jwt_token(secret_key=secret_key, exp_days=exp_days)

    def _generate_jwt_token(self, secret_key: str, exp_minutes: int = None, exp_days: int = None) -> str:
        iat_dt = datetime.now()
        algorithm = TokenConstants.algorithm()

        if exp_minutes:
            exp_dt = iat_dt + timedelta(minutes=exp_minutes)
        elif exp_days:
            exp_dt = iat_dt + timedelta(days=exp_days)
        else:
            raise ValueError("Either exp_minutes or exp_days must be provided")

        payload = {
            'user_id': str(self.id),
            'email': self.email,
            'is_premium': self.is_premium,
            'exp': int(exp_dt.timestamp()),
            'iat': int(iat_dt.timestamp()),
        }

        token = jwt.encode(payload, secret_key, algorithm=algorithm)

        if isinstance(token, bytes):
            token = token.decode('utf-8')

        return token

    class Meta:
        db_table = 'link_user'
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email'),
        ]


class Profile(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=16, choices=UserGenderChoices.choices, blank=True, null=True)
    image_url = models.CharField(blank=True, null=True, max_length=512)
    s3_key = models.CharField(blank=True, null=True, max_length=255)

    def __str__(self):
        return self.name

    @property
    def name(self) -> str:
        return f'{self.first_name} {self.last_name}'.strip() or "No Name Provided"

    class Meta:
        db_table = 'link_profile'
        ordering = ('-created_at',)
