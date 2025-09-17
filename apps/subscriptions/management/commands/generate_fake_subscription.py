import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from faker import Faker

from apps.subscriptions.helpers import StatusChoices, PlanChoices
from apps.subscriptions.models import Subscription
from apps.users.models import User
import time



class Command(BaseCommand):
    help = "Generate fake users with profiles"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count", type=int, default=10, help="Number of users to create"
        )

    def handle(self, *args, **options):
        fake = Faker()
        count = options["count"]
        start = time.time()
        users = list(User.objects.all())
        status_choices = [StatusChoices.ACTIVE, StatusChoices.INACTIVE]
        plan_choices = [PlanChoices.BASIC, PlanChoices.PREMIUM]

        for _ in range(count):
            user = random.choice(users)
            start_date = fake.date_time_between(start_date='-1y', end_date='now')
            end_date = start_date + timedelta(days=30) if random.choice([True, False]) else None

            Subscription.objects.create(
                user=user,
                status=random.choice(status_choices),
                plan=random.choice(plan_choices),
                start_date=start_date,
                end_date=end_date,
                stripe_customer_id=fake.uuid4()
            )
        end = time.time()
        self.stdout.write(self.style.SUCCESS(f"Took {end - start} seconds"))
        self.stdout.write(self.style.SUCCESS(f"✅ Created {count} fake users"))
