from rest_framework import serializers
from dataclasses import dataclass
from shared.cache import CacheService
from users.models import User


@dataclass
class ActivatorUserMeta:
    id: int


class ActivatorUserMetaSerializer(serializers.Serializer):
    id = serializers.IntegerField()


record: dict = CacheService().get(
    namespace="activateion", key="87bd4dd6-47ca-3eaa-bf30-047d06148063"
)
serializer = ActivatorUserMetaSerializer(data=record)
serializer.is_valid(raise_exception=True)

serializer.validated_data["id"]

user = User.objects.get(id=instance.id)
