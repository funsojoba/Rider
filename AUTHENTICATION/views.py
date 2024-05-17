from rest_framework import viewsets, status
from rest_framework.decorators import action
from helpers.response import Response

from AUTHENTICATION.serializers import UserSerializer
from AUTHENTICATION.service import AuthenticationService


class AuthViewSet(viewsets.ViewSet):
    @action(methods=["POST"], detail=False)
    def sign_up_user(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = AuthenticationService.create_viewer_user(
            **serializer.validated_data
        )
        return Response(
            data=UserSerializer(instance=user).data,
            status=status.HTTP_201_CREATED,
        )
