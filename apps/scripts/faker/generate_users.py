import os, django
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User, Profile

fake = Faker()

def generate_users(n=100):
    for _ in range(n):
        user = User.objects.create_user(
            email=fake.unique.email(),
            password='password123',
            is_active=True
        )
        Profile.objects.filter(user=user).update(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=70),
            gender=fake.random_element(elements=('male', 'female', 'other'))
        )
    print(f"{n} fake users created!")

if __name__ == "__main__":
    generate_users(100)
