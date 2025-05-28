from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_employee = models.BooleanField(default=False, verbose_name="Is employee")


    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = [
            "email",
        ]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email