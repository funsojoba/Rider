from __future__ import annotations

import uuid
from enum import Enum
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.db import models

# from helpers.db_helper import BaseAbstractModel

from django.contrib.gis.db import models as gis_models


def generate_id():
    return uuid.uuid4().hex


class UserTypes(Enum):
    ADMIN = "ADMIN"
    RIDER = "RIDER"
    USER = "USER"
    SUPER_ADMIN = "SUPER_ADMIN"


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

    def create_user(self, email, password=None, **extrafields):
        extrafields.setdefault("is_superuser", False)
        return self._create_user(email=email, password=password, **extrafields)

    def create_superuser(self, email, password=None, **extrafields):
        extrafields.setdefault("is_superuser", True)
        extrafields.setdefault("is_active", True)
        extrafields.setdefault("is_staff", True)
        return self._create_user(email=email, password=password, **extrafields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(
        primary_key=True, editable=False, default=generate_id, max_length=70
    )

    USER_TYPE = (
        ("ADMIN", "ADMIN"),
        ("RIDER", "RIDER"),
        ("USER", "USER"),
        ("SUPER_ADMIN", "SUPER_ADMIN"),
    )
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField(unique=True)

    phone_number = models.CharField(max_length=150)
    avatar = models.URLField(null=True, blank=True)

    city = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    country = models.CharField(max_length=256)

    user_type = models.CharField(
        choices=USER_TYPE, max_length=300, default="USER"
    )
    rating = models.FloatField(default=0)

    # user current location
    location = gis_models.PointField(null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    @property
    def display_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.display_name


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
