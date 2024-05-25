from .models import Ride
from Driver.models import RideDriver

from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance


User = get_user_model()


class RideService:
    @classmethod
    def get_customer_rides(cls, user: User):
        return Ride.objects.filter(
            customer=user,
        )

    @classmethod
    def get_driver_rides(cls, user: User):
        return Ride.objects.filter(
            driver=user,
        )

    @classmethod
    def get_nearby_driver(cls, location: dict):

        user_point = Point(
            location.get("longitue"), location.get("latitude"), srid=4326
        )
        drivers = (
            RideDriver.objects.filter(
                is_driver_verified=True,
            )
            .annotate(distance=Distance("driver__location", user_point))
            .order_by("distance")[:10]
        )
        return drivers
