import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from apps.users.models import User


@pytest.mark.django_db
def test_signup_creates_inactive_user_and_send_email(mocker):
    client = APIClient()
    url = reverse("signup")

    mock_send_email = mocker.patch("apps.users.serializers.auth_serializer.send_verification_email_task")

    response = client.post(url, {"email": "verifyme@yopmail.com", "password": "12345"}, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['message'] == 'User created successfully'
    user = User.objects.get(email="verifyme@yopmail.com")
    assert user.is_active is False
    mock_send_email.assert_called_once_with(user.id, 'testserver')