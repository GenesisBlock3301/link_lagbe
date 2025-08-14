from django.db import models
from apps.users.models import User
from apps.common.models import BaseModel
from apps.subscriptions.helpers import StatusChoices, PlanChoices


class Subscription(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    status = models.CharField(max_length=10, choices=StatusChoices.choices)
    plan = models.CharField(max_length=10, choices=PlanChoices.choices)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    stripe_customer_id = models.TextField()

    def __str__(self):
        return f"{self.user.email} - {self.status} ({self.plan})"

    class Meta:
        db_table = 'link_lagbe_subscription'
        ordering = ('-created_at',)

