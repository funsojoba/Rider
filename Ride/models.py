from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.auth import get_user_model

from helpers.db_helper import BaseAbstractModel


User = get_user_model()


class Ride(BaseAbstractModel):
    driver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="driver",
        related_name="driver_rides",
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="customer",
        related_name="customer_rides",
    )
    start_location = gis_models.PointField(verbose_name="start location")
    end_location = gis_models.PointField(verbose_name="end location")
    base_fare = models.FloatField(verbose_name="trip cost", default=0)
    distance = models.FloatField(verbose_name="distance")
    trip_time = models.DurationField(verbose_name="trip time")
    trip_start_time = models.DateTimeField(null=True, blank=True)
    trip_end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}"
