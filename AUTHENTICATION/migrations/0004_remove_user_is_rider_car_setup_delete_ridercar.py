# Generated by Django 4.2.13 on 2024-05-23 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("AUTHENTICATION", "0003_user_is_rider_car_setup_ridercar"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="is_rider_car_setup",
        ),
        migrations.DeleteModel(
            name="RiderCar",
        ),
    ]
