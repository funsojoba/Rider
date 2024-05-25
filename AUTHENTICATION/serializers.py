from rest_framework import serializers
from django.contrib.gis.geos import Point

from .models import User

from User.service import UserService


class UserSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True, required=False)
    longitude = serializers.FloatField(write_only=True, required=False)
    location = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        return UserService.get_user_rating(obj).get("rating")

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "avatar",
            "city",
            "state",
            "country",
            "user_type",
            "rating",
            "location",
            "latitude",
            "longitude",
            "is_staff",
            "is_admin",
            "is_superuser",
            "is_active",
            "created_at",
            "updated_at",
        ]

    def get_location(self, obj):
        return (
            {"latitude": obj.location.y, "longitude": obj.location.x}
            if obj.location
            else None
        )

    def create(self, validated_data):
        latitude = validated_data.pop("latitude", None)
        longitude = validated_data.pop("longitude", None)
        if latitude is not None and longitude is not None:
            validated_data["location"] = Point(longitude, latitude)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        latitude = validated_data.pop("latitude", None)
        longitude = validated_data.pop("longitude", None)
        if latitude is not None and longitude is not None:
            instance.location = Point(longitude, latitude)
        return super().update(instance, validated_data)


class MinimalUserSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        return UserService.get_user_rating(obj).get("rating")

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "avatar",
            "user_type",
            "rating",
        ]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
