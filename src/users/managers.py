from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(
        self,
        email: str,
        password: str,  # 1234
        **extra_fields,
    ):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        setattr(user, "password", make_password(password))

        # user.save(using=self._db)
        user.save()

        return user

    def create_superuser(self, email: str, password: str, **extra_fields):
        pass
