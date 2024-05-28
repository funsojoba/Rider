from .models import Ride
from Driver.models import RideDriver

from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance


User = get_user_model()


class RideService:
    """_summary_

    RIDE FLOW
    - Get current location (update user current location)
    - Select destination
    - Get nearby drivers
    - Select a driver
    - Driver is notified
    - Driver accepts / rejects
    - Customer is notified
    - Driver drives to customer location
    - Driver starts trip
    - Calculate trip cost based on
        - distance
        - time
        - surge (etc.)
    - Notify customer of price at different milestone
    - End trip
    - Customer pays
    - Customer rates driver
    - Driver rates customer

    - Can't book a ride if you're already in a ride
    - Can't see a driver if driver is already in a ride
    """

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
            float(location.get("long")), float(location.get("lat")), srid=4326
        )
        drivers = (
            RideDriver.objects.filter(
                is_driver_verified=True,
            )
            .annotate(distance=Distance("driver__location", user_point))
            .order_by("distance")[:10]
        )
        return drivers
