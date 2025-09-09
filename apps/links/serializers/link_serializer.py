from rest_framework import serializers
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from apps.links.models import Link


class LinkSerializer(serializers.ModelSerializer):
    click_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Link
        fields = ['id', 'user', 'title', 'url', 'order', 'click_count', 'created_at']
        read_only_fields = ['id', 'click_count', 'created_at']

    def validate_url(self, value):
        validator = URLValidator()
        try:
            validator(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Enter a valid URL.")
        return value


class UserLinkSerializer(serializers.ModelSerializer):
    click_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Link
        fields = ["id", "title", "url", "order", "click_count"]
