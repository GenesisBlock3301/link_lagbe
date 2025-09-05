from apps.users.tests.test_models import (test_create_superuser, test_create_user, test_user_token_generation,
                                          test_create_user_without_email_raises_error, test_profile_name_property)
from apps.users.tests.test_views import test_signup_creates_inactive_user_and_send_email
from apps.users.tests.test_serializers import test_user_signup_serializer_creates_inactive_user