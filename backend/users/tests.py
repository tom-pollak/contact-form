from django.test import TestCase
from django.contrib.auth import get_user_model

from tier.models import Tier

class UsersManagersTest(TestCase):
    def setUp(self):
        Tier.objects.create(pk=1, name="Free", no_forms=5, price=0.00)
        Tier.objects.create(pk=2, name="Intermediate", no_forms=50, price=2.49)
        Tier.objects.create(pk=3, name="Unlimited", no_forms=2147483647, price=4.99)

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')

        self.assertEqual(user.tier.name, 'Free')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        # username is None for the AbstractUser
        self.assertIsNone(user.username)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='foo')
            
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='foo', tier='Free')
        with self.assertRaises(ValueError):
            T = Tier.objects.get(name="Unlimited")
            User.objects.create_user(email='', password='foo', tier=T)
    
    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='super@user.com', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')

        self.assertEqual(admin_user.tier.name, 'Unlimited')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertIsNone(admin_user.username)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)
        
        with self.assertRaises(ValueError):
            T = Tier.objects.get(name="Free")
            User.objects.create_superuser(email='', password='foo', tier=T)