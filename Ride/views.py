from drf_yasg.utils import swagger_auto_schema

from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework import permissions, status

from .serializers import RideSerializer
from .service import RideService

from helpers.response import Response
from helpers.permissions import IsUser


class CustomerRideViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated, IsUser]

    @swagger_auto_schema(
        operation_description="Get all customer's rides",
        operation_summary="Get all customer's rides",
        tags=["Ride"],
    )
    @action(methods=["GET"], detail=False, url_path="customer-rides")
    def get_customer_rides(self, request):
        rides = RideService.get_customer_rides(user=request.user)
        return Response(
            data=RideSerializer(rides, many=True).data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_description="Get nearby drivers",
        operation_summary="Get nearby drivers",
        tags=["Ride"],
    )
    @action(methods=["GET"], detail=False, url_path="nearby-drivers")
    def get_nearby_drivers(self, request):
        location = request.query_params.dict()
        drivers = RideService.get_nearby_driver(location=location)
        return Response(
            data=RideSerializer(drivers, many=True).data,
            status=status.HTTP_200_OK,
        )


class DriverRideViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Get all driver's rides",
        operation_summary="Get all driver's rides",
        tags=["Ride"],
    )
    @action(methods=["GET"], detail=False, url_path="driver-rides")
    def get_driver_rides(self, request):
        rides = RideService.get_driver_rides(user=request.user)
        return Response(
            data=RideSerializer(rides, many=True).data,
            status=status.HTTP_200_OK,
        )
