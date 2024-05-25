from enum import Enum
from django.db import models

from django.contrib.auth import get_user_model

from Ride.models import Ride

from helpers.db_helper import BaseAbstractModel


User = get_user_model()


class RatingEnum(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class UserRating(BaseAbstractModel):
    rating = models.IntegerField(
        choices=((rating.value, rating.name) for rating in RatingEnum)
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_ratings"
    )
    rated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rated_by"
    )
    ride = models.ForeignKey(
        Ride, on_delete=models.CASCADE, related_name="ride_ratings"
    )
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.display_name}'s rating for {self.ride.id}"
