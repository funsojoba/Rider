from rest_framework import status

from django.db.models import Sum, Count
from django.contrib.gis.geos import Point

from AUTHENTICATION.models import User

from User.models import UserRating
from helpers.exceptions import CustomApiException


class UserService:
    @classmethod
    def get_user(cls, **kwargs) -> User:
        return User.objects.filter(**kwargs).first()

    @classmethod
    def update_user(cls, user, **kwargs):
        avatar = kwargs.get("avatar")
        user.first_name = kwargs.get("first_name", user.first_name)
        user.last_name = kwargs.get("last_name", user.last_name)
        user.email = kwargs.get("email", user.email)
        user.phone_number = kwargs.get("phone_number", user.phone_number)
        user.city = kwargs.get("city", user.city)
        user.state = kwargs.get("state", user.state)
        user.country = kwargs.get("country", user.country)

        if avatar:
            # TODO: upload avatar to AWS S3
            pass
        user.save()
        return user

    @classmethod
    def rate_user(cls, user: User, data: dict) -> UserRating:
        rating = UserRating.objects.filter(
            user__id=data.get("user_id"), ride__id=data.get("ride_id")
        ).first()

        if rating:
            raise CustomApiException(
                "You have already rated this user",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        rating = UserRating.objects.create(
            rated_by=user,
            user_id=data.get("user_id"),
            ride_id=data.get("ride_id"),
            rating=data.get("rating"),
            comment=data.get("comment"),
        )
        return rating

    @classmethod
    def get_user_rating(cls, user: User) -> UserRating:
        user_rating = UserRating.objects.filter(user=user).aggregate(
            total_rating=Sum("rating"), count_rating=Count("rating")
        )

        total_rating = user_rating["total_rating"]
        count_rating = user_rating["count_rating"]
        average_rating = total_rating / count_rating if count_rating else 0

        return {"rating": average_rating}

    @classmethod
    def update_user_locatio(cls, location: dict, user: User) -> None:
        user_point = Point(
            float(location.get("long")), float(location.get("lat")), srid=4326
        )
        user = User.location = user_point
        user.save()
