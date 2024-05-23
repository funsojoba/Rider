# Generated by Django 4.2.13 on 2024-05-23 10:54

import AUTHENTICATION.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("AUTHENTICATION", "0002_user_location_user_rating"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_rider_car_setup",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="RiderCar",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=AUTHENTICATION.models.generate_id,
                        editable=False,
                        max_length=70,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "car_number",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                (
                    "car_model",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                (
                    "car_color",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                (
                    "car_plate_number",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                ("car_picture", models.URLField(blank=True, null=True)),
                (
                    "car_year",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "rider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cars",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
