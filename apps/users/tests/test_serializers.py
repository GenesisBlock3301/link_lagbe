import pytest
from apps.users.serializers.auth_serializer import (
    UserSignupSerializer
)
from apps.users.models import User


# Use monkeypatch to mock email task
@pytest.mark.django_db
def test_user_signup_serializer_creates_inactive_user(monkeypatch):
    called = {}

    # Mock send_verification_email_task
    def dummy_task(user_id, domain):
        called['yes'] = (user_id, domain)

    monkeypatch.setattr(
        "apps.users.serializers.auth_serializer.send_verification_email_task",
        dummy_task
    )

    data = {
        "email": "testuser@example.com",
        "password": "password123"
    }

    serializer = UserSignupSerializer(data=data, context={
        "request": type("Request", (), {"get_host": lambda self: "testserver"})()})
    assert serializer.is_valid(), serializer.errors
    user = serializer.save()

    # DB assertions
    assert User.objects.filter(email="testuser@example.com").exists()
    assert user.is_active is False
    assert user.profile is not None

    # Task was called
    assert called['yes'][0] == user.id
    assert called['yes'][1] == "testserver"
