from django.db import models

from .managers import TierManager

class Tier(models.Model):
    objects = TierManager()
    name = models.CharField(max_length=100, unique=True)
    no_forms = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)