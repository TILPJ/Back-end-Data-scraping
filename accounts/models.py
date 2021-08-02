from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number", "date_of_birth"]

    objects = CustomUserManager()

    phone_number = models.CharField(max_length=11, blank=False, unique=True)
    date_of_birth = models.CharField(max_length=8, blank=False)

    def __str__(self):
        return self.email
