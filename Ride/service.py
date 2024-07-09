from .models import Ride
from Driver.models import RideDriver
from Ride.models import Ride

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from Driver.service import RideDriverService

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
        """
            A service to return top 10 drivers that are closest
            to the User
        """

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

    @classmethod
    def get_destination_point(cls, destination:dict):
        # Idea here is to retrieve location point from say Google Map based on User's location input
        pass

    @classmethod
    def start_trip(cls, trip: Ride):
        now = timezone.now()
        trip.trip_start_time = now
        trip.save()

        # Websocket notify User about the trip starting

    def end_trip(cls):
        # set trip_end_time
        # get actual distance
        # get actual time
        # calculate time_amount
        # calculate trip amount
        pass

    @classmethod
    def initiate_ride(cls, user:User, driver_id:str, start_location:dict, end_location:dict):
        # This is for a user, when they click on start ride
        # a websocket notification is sent to the selected 
        # driver of which they accept or reject

        # get driver instance and notify
        driver = RideDriverService.get_driver_by_id(driver_id=driver_id)
        start_location = Point(
            float(start_location.get("long")), 
            float(start_location.get("lat")), 
            srid=4326
        )
        
        end_location = Point(
            float(end_location.get("long")), 
            float(end_location.get("lat")), 
            srid=4326
        )

        # Distance, might be wrong
        # distance = Distance(end_location - start_location)
        
        ride = Ride(
            customer=user,
            driver=driver,
            start_location=start_location,
            end_location=end_location
        )

        # websocket notify selected user

    @classmethod
    def calculate_trip_amount(cls, ride: Ride, discount:dict =None) -> dict:
        """
            Rough calculation for trip amount, to flesh out later
        """
        distance = ride.distance
        distance_amount = distance * 10 # say we charge 10 naira per km or whatever
        
        trip_time = ride.trip 
        trip_time_amount = trip_time * 10 # say we charge 10 naira per say minutes or 30 minutes
        base_fare = ride.base_fare
        discount = 0

        if discount:
            # verify discount code
            discount = discount.get("code") if discount.get("code") else 0

        total_amount = (distance_amount + trip_time_amount + base_fare) - discount

        return {
            "distance": distance_amount,
            "trip_time": trip_time_amount,
            "total_amount": total_amount,
            "discount": discount
        }
        


        


