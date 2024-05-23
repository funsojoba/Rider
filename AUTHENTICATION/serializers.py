from rest_framework import serializers

from .models import User, RiderCar


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ["id"]
        exclude = [
            "avatar",
            "group",
            "permissions",
        ]
        extra_kwargs = {"password": {"write_only": True}}


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RiderCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiderCar
        read_only_fields = ["id"]
        exclude = ["rider"]
