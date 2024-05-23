from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework import permissions, status

from .serializers import RideDriverSerializer
from .service import RideDriverService

from helpers.permissions import IsRider
from helpers.response import Response


class DriverViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated, IsRider]

    @swagger_auto_schema(
        operation_description="Set up driver information",
        operation_summary="Set up driver information",
        tags=["Driver"],
        request_body=RideDriverSerializer,
    )
    @action(methods=["POST"], detail=False, url_path="setup-driver")
    def set_up_driver(self, request):
        serializer = RideDriverSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rider_car = RideDriverService.setup_driver_details(
            user=request.user, driver_details=serializer.validated_data
        )
        return Response(
            data=RideDriverSerializer(rider_car).data,
            status=status.HTTP_200_OK,
        )
