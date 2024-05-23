from rest_framework import viewsets, status
from rest_framework.decorators import action
from helpers.response import Response

from AUTHENTICATION.serializers import (
    UserSerializer,
    LoginSerializer,
    RiderCarSerializer,
)
from AUTHENTICATION.service import AuthenticationService


class AuthViewSet(viewsets.ViewSet):
    @action(methods=["POST"], detail=False)
    def sign_up_user(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_type = serializer.validated_data.pop("user_type")

        if user_type == "RIDER":
            user = AuthenticationService.create_rider_user(
                **serializer.validated_data
            )
        else:
            user = AuthenticationService.create_customer_user(
                **serializer.validated_data
            )
        return Response(
            data=UserSerializer(instance=user).data,
            status=status.HTTP_201_CREATED,
        )

    @action(methods=["POST"], detail=False)
    def login_user(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        login_user = AuthenticationService.login_user(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        return login_user

    @action(methods=["POST"], detail=False)
    def setup_rider_car_details(self, request):
        serializer = RiderCarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rider_car = AuthenticationService.setup_rider_car_details(
            **serializer.validated_data
        )
        return Response(
            data=RiderCarSerializer(rider_car).data, status=status.HTTP_200_OK
        )
