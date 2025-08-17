from django.contrib import admin

# Register your models here.
from apps.links.models import Link, LinkClick

admin.site.register(Link)
admin.site.register(LinkClick)
