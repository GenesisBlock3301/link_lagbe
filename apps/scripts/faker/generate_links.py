import os, django
from faker import Faker
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.links.models import Link
from apps.users.models import User

fake = Faker()

def generate_links(n=200):
    users = list(User.objects.all())
    for _ in range(n):
        user = random.choice(users)
        Link.objects.create(
            user=user,
            title=fake.sentence(nb_words=4),
            url=fake.url(),
            order=random.randint(1, 100)
        )
    print(f"{n} fake links created!")

if __name__ == "__main__":
    generate_links(200)
