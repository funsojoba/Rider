from rest_framework import serializers

from .models import Ride

from AUTHENTICATION.serializers import MinimalUserSerializer


class RideSerializer(serializers.ModelSerializer):
    driver = MinimalUserSerializer(read_only=True)
    customer = MinimalUserSerializer(read_only=True)

    class Meta:
        model = Ride
        fields = "__all__"
