import uuid
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from AUTHENTICATION.models import User, UserTypes


def generate_id():
    return uuid.uuid4().hex


class RideDriver(models.Model):
    id = models.CharField(
        primary_key=True, editable=False, default=generate_id, max_length=70
    )
    driver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="ride_driver"
    )
    drivers_license_picture = models.URLField(null=True, blank=True)
    drivers_license_number = models.CharField(
        max_length=256, null=True, blank=True
    )
    is_drivers_licence_valid = models.BooleanField(default=False)

    # driver's physical address
    home_address = models.CharField(max_length=256, null=True, blank=True)

    # driver's car details
    car_number = models.CharField(max_length=256, null=True, blank=True)
    car_model = models.CharField(max_length=256, null=True, blank=True)
    car_color = models.CharField(max_length=256, null=True, blank=True)
    car_plate_number = models.CharField(max_length=256, null=True, blank=True)
    car_picture = models.URLField(null=True, blank=True)
    car_year = models.CharField(max_length=256, null=True, blank=True)
    car_brand = models.CharField(max_length=256, null=True, blank=True)
    is_rider_car_setup = models.BooleanField(default=False)

    is_driver_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "DRIVER - " + self.driver.display_name


@receiver(post_save, sender=User)
def _post_save_receiver(sender, instance, created, **kwargs):
    if created and instance.user_type == UserTypes.RIDER.value:
        user_rider = RideDriver.objects.filter(rider=instance).first()
        if not user_rider:
            RideDriver.objects.create(driver=instance)
