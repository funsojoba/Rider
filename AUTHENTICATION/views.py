from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from helpers.response import Response

from AUTHENTICATION.serializers import UserSerializer, LoginSerializer
from AUTHENTICATION.service import AuthenticationService


class AuthViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="Sign Up User",
        operation_summary="Sign Up User",
        tags=["Auth"],
        request_body=UserSerializer,
    )
    @action(methods=["POST"], detail=False, url_path="sign-up")
    def sign_up_user(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_type = serializer.validated_data.pop("user_type")

        switcher = {
            "RIDER": AuthenticationService.create_rider_user,
            "CUSTOMER": AuthenticationService.create_customer_user,
        }
        user = switcher.get(user_type, lambda: None)(
            **serializer.validated_data
        )
        return Response(
            data=UserSerializer(instance=user).data,
            status=status.HTTP_201_CREATED,
        )

    @swagger_auto_schema(
        operation_description="Log In User",
        operation_summary="Log In User",
        tags=["Auth"],
        request_body=LoginSerializer,
    )
    @action(methods=["POST"], detail=False, url_path="login")
    def login_user(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        login_user = AuthenticationService.login_user(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        return login_user

    @swagger_auto_schema(
        operation_description="Get User Details",
        operation_summary="Get User Details",
        tags=["Auth"],
    )
    @action(methods=["GET"], detail=False, url_path="me")
    def get_user(self, request):
        AuthenticationService.get_user(id=request.user.id)
        return Response(
            data=UserSerializer(instance=request.user).data,
            status=status.HTTP_200_OK,
        )
