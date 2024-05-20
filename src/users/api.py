import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import generics, permissions, serializers, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from users.enums import Role

from .services import Activator

# from . import services

User = get_user_model()
# == from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "role"]

    def validate_role(self, value: str) -> str:
        if value not in Role.users():
            raise ValidationError(
                f"Selected Role must be in {Role.users_values()}",
            )
        return value

    def validate(self, attrs: dict) -> dict:
        """Change the password for its hash"""

        attrs["password"] = make_password(attrs["password"])

        return attrs


class UserRegistrationPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "role"]


class UserListCreateAPI(generics.ListCreateAPIView):
    http_method_names = ["get", "post"]
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return User.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Functional approach
        # activation_key: uuid.UUID = services.create_activation_key(
        #     email=serializer.data["email"]
        # )
        # services.send_user_activation_email(
        #     email=serializer.data["email"], activation_key=activation_key
        # )

        # OOP approach
        activator_service = Activator(email=serializer.data["email"])
        activation_key = activator_service.create_activation_key()
        activator_service.send_user_activation_email(
            activation_key=activation_key
        )
        activator_service.save_activation_information(
            internal_user_id=serializer.instance.id,
            activation_key=activation_key,
        )

        return Response(
            UserRegistrationPublicSerializer(serializer.validated_data).data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data),
        )

    def get(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=self.get_success_headers(serializer.data),
        )


@api_view(http_method_names=["POST"])
def resend_activation_mail(request) -> Response:
    breakpoint()
    pass


# def create_user(request: HttpRequest) -> JsonResponse:
#     if request.method != "POST":
#         raise NotImplementedError("Only POST requests")

#     data: dict = json.loads(request.body)
#     user = User.objects.create_user(**data)

#     # convert to dict
#     results = {
#         "id": user.id,
#         "email": user.email,
#         "first_name": user.first_name,
#         "last_name": user.last_name,
#         "role": user.role,
#         "is_active": user.is_active,
#     }

#     return JsonResponse(results)



import asyncio
import time
from django.http import JsonResponse


async def foo(request):
    await asyncio.sleep(5)

    return JsonResponse(data={"message": "Hello"})
