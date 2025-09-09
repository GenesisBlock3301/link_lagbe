import random, time
from faker import Faker
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.links.models import Link, LinkClick
from apps.users.models import User


class Command(BaseCommand):
    help = "Generate fake links with optional clicks"

    def add_arguments(self, parser):
        parser.add_argument("--links", type=int, default=100, help="Number of links to create")
        parser.add_argument("--clicks", type=int, default=500, help="Number of clicks to create")

    def handle(self, *args, **options):
        fake = Faker()
        num_links = options["links"]
        num_clicks = options["clicks"]

        start = time.time()

        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.ERROR("❌ No users found. Please seed users first."))
            return

        with transaction.atomic():
            # ---- Bulk Create Links ----
            links = [
                Link(
                    user=random.choice(users),
                    title=fake.sentence(nb_words=4),
                    url=fake.url(),
                    order=random.randint(1, 100),
                )
                for _ in range(num_links)
            ]
            Link.objects.bulk_create(links, batch_size=500)

            # Fetch links back (most recent ones)
            links = list(Link.objects.order_by("-id")[:num_links])

            # ---- Bulk Create LinkClicks ----
            clicks = [
                LinkClick(
                    link=random.choice(links),
                    user_ip=fake.ipv4_public(),
                )
                for _ in range(num_clicks)
            ]
            LinkClick.objects.bulk_create(clicks, batch_size=1000)

        end = time.time()
        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Created {num_links} links and {num_clicks} clicks in {end - start:.2f}s"
            )
        )
