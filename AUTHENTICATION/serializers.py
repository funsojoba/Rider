from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        write_only_fields = ["password"]
        readonly_fields = ["id"]
        exclude = ["avatar"]
