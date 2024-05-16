from drf_yasg.utils import swagger_auto_schema

from .serializers import UserCreateSerializer

user_create = swagger_auto_schema(
    methods=["put", "post"], request_body=UserCreateSerializer
)
