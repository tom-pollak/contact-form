from django.test import TestCase
from django.contrib.auth import get_user_model
from tiers.models import Tier

from .models import Form#, Submissions

class FormTest(TestCase):

    def setUp(self):
        User = get_user_model()
        Tier.objects.create(pk=1, name="Free", no_forms=5, price=0.00)
        self.user = User.objects.create_user(email='normal@user.com', password='foo')

    def test_create_form(self):
        form = Form.objects.create(
            name='Test', url='https://test.com', test_period=5, created_by=self.user
        )

        self.assertEqual(str(form), 'Test')
