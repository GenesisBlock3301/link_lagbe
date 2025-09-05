from django.db import models
from apps.users.models import User
from apps.common.models import BaseModel


class Link(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='links')
    title = models.CharField(max_length=100)
    url = models.URLField()
    order = models.PositiveIntegerField(default=0)

    def click_count(self):
        return self.clicks.count()

    def __str__(self):
        return f"{self.title} ({self.user.email})"

    class Meta:
        db_table = 'link_lagbe_link'
        ordering = ('-created_at',)


class LinkClick(BaseModel):
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name='clicks')
    clicked_at = models.DateTimeField(auto_now_add=True)
    user_ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"Click on {self.link.title} at {self.clicked_at}"

    class Meta:
        db_table = 'link_lagbe_link_click'
        ordering = ('-created_at',)
