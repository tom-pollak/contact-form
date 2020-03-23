from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager
from tier.models import Tier

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, null=True, default=None)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email