import pytest
from apps.users.models import User
from apps.users.helpers import TokenConstants


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(email="test@example.com", password="password123", is_active=True)

    assert user.email == "test@example.com"
    assert user.is_active is True
    assert user.profile is not None  # Profile should be created automatically
    assert user.check_password("password123")  # Password is hashed correctly


@pytest.mark.django_db
def test_create_user_without_email_raises_error():
    with pytest.raises(TypeError):
        User.objects.create_user(password="password123")


@pytest.mark.django_db
def test_create_superuser():
    superuser = User.objects.create_superuser(email="admin@example.com", password="adminpass")

    assert superuser.is_superuser is True
    assert superuser.is_staff is True
    assert superuser.is_active is True


@pytest.mark.django_db
def test_profile_name_property():
    user = User.objects.create_user(email="user@example.com", password="pass")
    profile = user.profile
    profile.first_name = "John"
    profile.last_name = "Doe"
    profile.save()

    assert profile.name == "John Doe"


@pytest.mark.django_db
def test_user_token_generation():
    user = User.objects.create_user(email="tokenuser@example.com", password="pass")
    secret_key = "mysecretkey"

    access_token = user.token(secret_key=secret_key)
    refresh_token = user.refresh_token(secret_key=secret_key)

    assert access_token is not None
    assert refresh_token is not None

    # Optional: decode JWT to verify payload
    import jwt
    decoded = jwt.decode(access_token, secret_key, algorithms=[TokenConstants.algorithm()])
    assert decoded['user_id'] == str(user.id)
    assert decoded['email'] == user.email
