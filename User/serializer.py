from rest_framework import serializers
from User.models import RatingEnum


class RateSerializer(serializers.Serializer):

    rating = serializers.ChoiceField(
        choices=[(rating.value, rating.name) for rating in RatingEnum]
    )

    comment = serializers.CharField(required=False)
    ride_id = serializers.CharField()
    user_id = serializers.CharField()
