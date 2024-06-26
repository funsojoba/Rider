# import uuid
from .models import User

# from django.conf import settings
from django.contrib.auth.hashers import check_password

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

# from helpers.generate_otp import get_otp
from helpers.cache_manager import CacheManager
from helpers.response import Response

from .serializers import UserSerializer


class AuthenticationService:
    @classmethod
    def _create_user(cls, user_type, **kwargs) -> User:
        # otp = get_otp()
        password = kwargs.get("password")

        user = User.objects.create(
            first_name=kwargs.get("first_name"),
            last_name=kwargs.get("last_name"),
            phone_number=kwargs.get("phone_number"),
            email=kwargs.get("email"),
            avatar=kwargs.get("avatar", ""),
            city=kwargs.get("city"),
            state=kwargs.get("state"),
            country=kwargs.get("country"),
            user_type=user_type,
        )
        user.set_password(password)
        user.save()

        # TODO: hash OTP before passing to cache
        # CacheManager.set_key(
        #     f"user:otp:{otp}",
        #     {"email": user.email},
        #     86400,
        # )
        # EmailService.send_async(
        #     template="verify_signup.html",
        #     subject="Verify Account",
        #     recipients=[user.email],
        #     context={"first_name": user.first_name, "otp": otp},
        # )
        return UserSerializer(instance=user).data

    @classmethod
    def create_admin_user(cls, **kwargs) -> User:
        user = cls._create_user("ADMIN", **kwargs)
        return user

    @classmethod
    def create_customer_user(cls, **kwargs) -> User:
        user = cls._create_user("USER", **kwargs)
        return user

    @classmethod
    def create_rider_user(cls, **kwargs) -> User:
        user = cls._create_user(user_type="RIDER", **kwargs)

        return user

    @classmethod
    def activate_user(cls, email: str) -> None:
        user = User.objects.filter(email=email).first()
        user.is_active = True
        user.save()

    # @classmethod
    # def verify_signed_up_user(cls, email, otp):
    #     # TODO: verify hashed OTP
    #     cached_info = CacheManager.retrieve_key(f"user:otp:{otp}")
    #     if cache_info and cache_info.get("email") == email:
    #         cls.activate_user(email)
    #         CacheManager.delete_key(f"user:reset_password:{otp}")
    #         user = cls.get_user(email=email)
    #         # EmailService.send_async(
    #         #     "complete_signup.html",
    #         #     "Welcome Onboard",
    #         #     [email],
    #         #     {
    #         #         "first_name": user.first_name.capitalize(),
    #         #     },
    #         # )
    #         return True
    #     return False

    @classmethod
    def set_user_password(cls, user, password):
        user.set_password(password)
        user.save()

    @classmethod
    def verify_user(cls, otp, email):
        otp = CacheManager.retrieve_key(f"user:otp:{otp}")
        if otp and otp.get("email") == email:
            CacheManager.delete_key(
                f"user:otp:{otp}"
            )  # TODO: delete key is not working for now
            user = cls.get_user(email=email).first()
            user.is_active = True
            user.save()
            return True
        return False

    # @classmethod
    # def forogt_password(cls, email):
    #     user = cls.get_user(email=email)

    #     if user:
    #         code = uuid.uuid4().hex
    #         verification_link = (
    #             f"{settings.BASE_URL}/verify-user?code={code}&email={email}"
    #         )
    #         CacheManager.set_key(
    #             f"user:reset_password:{code}",
    #             {"email": user.email},
    #             86400,
    #         )
    # EmailService.send_async(
    #     "forgot_password.html",
    #     "Forgot Password",
    #     [email],
    #     {
    #         "first_name": user.first_name.capitalize(),
    #         "verification_link": verification_link,
    #     },
    # )
    #     return True
    # return False

    @classmethod
    def verify_reset_password(cls, code, email):
        code = CacheManager.retrieve_key(f"user:reset_password:{code}")
        if code and code.get("email") == email:
            # NOTE: This delete_key is misbehaving
            CacheManager.delete_key(f"user:reset_password:{code}")
            return True
        return False

    @classmethod
    def reset_password(cls, password, email, code):
        verify_code = cls.verify_reset_password(code, email)
        if verify_code:
            user = cls.get_user(email=email)
            password = cls.set_user_password(user, password)
            return True
        return False

    @classmethod
    def get_user(cls, email: str) -> User:
        return User.objects.filter(email=email).first()

    @classmethod
    def login_user(cls, email, password):
        user = cls.get_user(email=email)

        if user:
            user_password = check_password(password, user.password)

            if not user_password:
                return Response(errors={"error": "incorrect email/password"})

            token = RefreshToken.for_user(user)
            data = {
                "user": UserSerializer(instance=user).data,
                "token": {
                    "refresh": str(token),
                    "access": str(token.access_token),
                },
            }
            return Response(data=data)
        return Response(
            errors={"error": "User does not exist"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @classmethod
    def get_all_users(cls, **kwargs):
        return User.objects.filter(**kwargs)

    # @classmethod
    # def set_user_avatar(cls, user, avatar):
    #     # user.avatar = avatar
    #     # user.save()
    #     avatar_uploader = AWSFileUploadManger()
    #     avatar_uploader.upload_file_object(
    #         file_object=avatar.file, file_name=avatar._name
    #     )
    #     return user

    @classmethod
    def set_user_avatar_cloudinay(cls, user, avatar):
        from helpers.cloudinary import CloudinaryManager

        image_upload = CloudinaryManager.upload_image(avatar, "davent/avatar")
        user.avatar = image_upload
        user.save()
        return user
