from celery import shared_task

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from apps.users.models import User

@shared_task
def send_verification_email_task(user_id, domain):
    user = User.objects.get(pk=user_id)

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    verification_link = f"http://{domain}/users/verify-email/{uid}/{token}/"

    subject = "Verify your email address"
    message = f"Hello {user.email},\n\nPlease click the link below to verify your account:\n{verification_link}"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )



@shared_task
def send_otp_email(email, otp):
    send_mail(
        subject="Your Password Reset OTP",
        message=f"Your OTP for password reset is {otp}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )