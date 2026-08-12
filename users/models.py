from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):

    username = None

    email = models.EmailField(unique=True)

    is_verified = models.BooleanField(default=False)

    ROLE_USER = "user"
    ROLE_MANAGER = "manager"

    ROLE_CHOICES = [
        (ROLE_USER, "Пользователь"),
        (ROLE_MANAGER, "Менеджер"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_USER,
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def is_manager(self):
        return self.role == self.ROLE_MANAGER
