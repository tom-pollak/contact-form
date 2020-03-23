from django.db import models

class TierManager(models.Manager):
    """
    Enables getting tiers through tier names rather than pk
    """
