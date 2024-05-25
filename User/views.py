from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action

from helpers.response import Response

from AUTHENTICATION.serializers import UserSerializer

from .service import UserService
from .serializer import RateSerializer


class UserViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="Get User Details",
        operation_summary="Get User Details",
        tags=["User"],
    )
    @action(methods=["GET"], detail=False, url_path="me")
    def get_user(self, request):
        user = UserService.get_user(id=request.user.id)
        return Response(
            data=UserSerializer(user).data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_description="Rate User",
        operation_summary="Rate User",
        tags=["User"],
        request_body=RateSerializer,
    )
    @action(methods=["POST"], detail=False, url_path="rate-user")
    def rate_user(self, request):
        serializer = RateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserService.rate_user(**serializer.validated_data)
        return Response(
            data=UserSerializer(user).data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_description="Get user rating",
        operation_summary="Rate User",
        tags=["User"],
    )
    @action(methods=["GET"], detail=False, url_path="get-rating")
    def get_user_rating(self, request):
        user_rating = UserService.get_user_rating(user=request.user)
        return Response(
            data=user_rating,
            status=status.HTTP_200_OK,
        )
