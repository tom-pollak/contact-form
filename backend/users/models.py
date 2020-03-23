from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager
from tier.models import Tier

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    tier = models.ForeignKey(Tier, to_field='name', on_delete=models.SET_DEFAULT, default=1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email