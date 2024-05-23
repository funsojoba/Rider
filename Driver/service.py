from .models import RideDriver
from AUTHENTICATION.models import User


class RideDriverService:
    @classmethod
    def setup_driver_details(
        cls, user: User, driver_details: dict
    ) -> RideDriver:
        # TODO: upload picture to AWS S3
        # TODO: SET UP DRIVER, WITH LICENSE VALIDATAION, ADDRESS VALIDATION,
        # AND MAYBE GUARANTOR DETAILS AND ALL
        # TODO: This code is full of error, fix it
        ride_driver = RideDriver.objects.filter(driver=user).first()

        car_picture = None
        drivers_license_picture = None
        if driver_details.get("car_picture"):
            # upload picture to wherever and get the link
            car_picture = "https://placehold.co/600x400/png"

        if driver_details.get("drivers_license_picture"):
            # upload picture to wherever and get the link
            drivers_license_picture = "https://placehold.co/600x400/png"
        if ride_driver:
            ride_driver.drivers_license_number = drivers_license_picture
            ride_driver.home_address = driver_details.get("home_address")
            ride_driver.car_number = driver_details.get("car_number")
            ride_driver.car_model = driver_details.get("car_model")
            ride_driver.car_color = driver_details.get("car_color")
            ride_driver.car_plate_number = driver_details.get(
                "car_plate_number"
            )
            ride_driver.car_brand = driver_details.get("car_brand")
            ride_driver.car_year = driver_details.get("car_year")
            ride_driver.car_picture = car_picture
            ride_driver.save()

            # TODO: rider_car_setup to be determined on car verification
            user.is_rider_car_setup = True
            user.save()
            return ride_driver
        else:
            rider_car = RideDriver.objects.create(
                driver=user,
                drivers_license_number=drivers_license_picture,
                home_address=driver_details.get("home_address"),
                car_number=driver_details.get("car_number"),
                car_model=driver_details.get("car_model"),
                car_color=driver_details.get("car_color"),
                car_plate_number=driver_details.get("car_plate_number"),
                car_brand=driver_details.get("car_brand"),
                car_year=driver_details.get("car_year"),
                car_picture=car_picture,
            )
            return rider_car
