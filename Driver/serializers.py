from .models import RideDriver
from rest_framework import serializers


class RideDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideDriver
        read_only_fields = ["id"]
        exclude = ["driver"]
