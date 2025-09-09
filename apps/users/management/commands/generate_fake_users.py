from django.core.management.base import BaseCommand
from faker import Faker
from apps.users.models import User, Profile


class Command(BaseCommand):
    help = "Generate fake users with profiles"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count", type=int, default=10, help="Number of users to create"
        )

    def handle(self, *args, **options):
        fake = Faker()
        count = options["count"]

        for _ in range(count):
            user = User.objects.create_user(
                email=fake.unique.email(),
                password="password123",
                is_active=True,
            )
            Profile.objects.filter(user=user).update(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=70),
                gender=fake.random_element(elements=("male", "female", "other")),
            )

        self.stdout.write(self.style.SUCCESS(f"✅ Created {count} fake users"))
