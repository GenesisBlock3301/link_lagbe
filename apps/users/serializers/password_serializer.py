from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class SendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist")
        return value


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Invalid email or OTP")
        cached_otp = cache.get(f"forgot_password_otp:{email}")
        if not cached_otp or cached_otp != otp:
            raise serializers.ValidationError("Invalid email or OTP")

        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email")

        cached_otp = cache.get(f"forgot_password_otp:{user.email}")
        if not cached_otp or cached_otp != otp:
            raise serializers.ValidationError("Invalid email or OTP")

        return attrs

    def save(self):
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return user
