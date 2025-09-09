import os, django
from faker import Faker
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.subscriptions.models import Subscription
from apps.users.models import User
from apps.subscriptions.helpers import StatusChoices, PlanChoices

fake = Faker()

def generate_subscriptions(n=100):
    users = list(User.objects.all())
    status_choices = [StatusChoices.ACTIVE, StatusChoices.INACTIVE]
    plan_choices = [PlanChoices.BASIC, PlanChoices.PREMIUM]

    for _ in range(n):
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
    print(f"{n} fake subscriptions created!")

if __name__ == "__main__":
    generate_subscriptions(100)
