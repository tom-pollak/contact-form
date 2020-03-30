from django.test import TestCase
from .models import Tier

class TierTest(TestCase):
    
    def test_create_tier(self):
        tier = Tier.objects.create(name='Test', no_forms=100, price=5.00)
        self.assertEqual(str(tier), 'Test')