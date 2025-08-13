from django.db import models


class StatusChoices(models.TextChoices):
    ACTIVE = 'active', 'Active'
    CANCELLED = 'cancelled', 'Cancelled'
    TRIAL = 'trial', 'Trial'


class PlanChoices(models.TextChoices):
    FREE = 'free', 'Free'
    PREMIUM = 'premium', 'Premium'