from django.db import models

class Tier(models.Model):
    name = models.CharField(max_length=100)
    no_forms = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name