import json
import uuid

import redis
from django.conf import settings

from .tasks import send_activation_mail
from shared.cache import CacheService


class Activator:
    def __init__(self, email: str):
        self.email = email

    def create_activation_key(self) -> uuid.UUID:
        return uuid.uuid3(namespace=uuid.uuid4(), name=self.email)

    def create_activation_link(self, activation_key: uuid.UUID) -> str:
        return f"https://frontend.com/users/activate/{activation_key}"

    def send_user_activation_email(self, activation_key: uuid.UUID) -> None:
        """Send activation email using SMTP."""

        activation_link = self.create_activation_link(activation_key)

        send_activation_mail.delay(
            recipient=self.email,
            activation_link=activation_link,
        )

    def save_activation_information(
        self, internal_user_id: int, activation_key: uuid.UUID
    ) -> None:
        """Save activation information to the cache.

        1. Connect to the cache

        2. Save the next structure to the cache:
        {
            "activation:a52a99ab-3631-4dae-befb-866beb5b8b52": {
                "user_id": 3
            }
        }

        3. Return None
        """

        # create Redis Connection instance
        # save record to the Redis with TTL of 1 day

        cache = CacheService()
        payload = {"user_id": internal_user_id}
        cache.save(
            namespace="activation",
            key=str(activation_key),
            instance=payload,
            ttl=2_000,
        )

    def validate_activation(self, activation_key: uuid.UUID) -> None:
        """Validate the activation UUID in the cache with requested.

        1. Build the key in the activation namespace:
            activation:a52a99ab-3631-4dae-befb-866beb5b8b52

        2. Retrieve record from the cache
        3. 404 if does not exist or the generation TTL is > 1 day
        4. 200 if exists & update user.is_active => True
        """

        # create Redis Connection instance
        # Generate the key base on the activation namespaces
        # udpate user table. is_active = True

        raise NotImplementedError
