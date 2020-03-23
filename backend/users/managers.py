from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

from tier.models import Tier

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email unique identifiers for
    authentication instead of usernames
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with given email and password
        """
        if not email:
            raise ValueError(_('Email must be set'))
        email = self.normalize_email(email)

        if not extra_fields.get('tier'):
            T = Tier.objects.get(name='Free')
            extra_fields.setdefault('tier', T)

            if str(extra_fields.get('tier')) != 'Free':
                raise ValueError(_('User must have free tier'))

        if extra_fields.get('tier') is None:
            raise ValueError(_('User must have a tier.'))

        if (extra_fields.get('is_superuser') is not True) and (str(extra_fields.get('tier')) != 'Free'):
            raise ValueError(_('User must be created with Free tier'))

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save SuperUser with given email and password
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        T = Tier.objects.get(name='Unlimited')
        extra_fields.setdefault('tier', T)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('SuperUser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('SuperUser must have is_superuser=True.'))

        if str(extra_fields.get('tier')) != 'Unlimited':
            raise ValueError(_('SuperUser must have unlimited tier.'))
        return self.create_user(email, password, **extra_fields)