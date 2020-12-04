# External Import
from djongo import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from rest_framework_simplejwt.tokens import RefreshToken

# Internal Import
from subscription.models import Subscription


class UserManager(BaseUserManager):
    """Manager for user profile"""

    def create_user(self, username, email, password=None):
        """Create a new user profile"""
        if username is None:
            raise ValueError('User must have a username')
        if email is None:
            raise ValueError('User must have a Email')

        email = self.normalize_email(email)

        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password=None):
        """Create and save a new superuser with given details"""
        if password is None:
            raise ValueError('Password should not be none')

        user = self.create_user(username, email, password)

        user.is_superuser = True
        user.is_staff = True

        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_verified = models.BooleanField(default=False)
    is_online = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    subscription = models.ForeignKey(
        Subscription, on_delete=models.SET_NULL, null=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        """Return string representation of the user's username"""
        return self.username

    def tokens(self):
        """ Genreate Access and Refresh Token for current user """
        user_token = RefreshToken.for_user(self)
        return {
            'refresh': str(user_token),
            'access': str(user_token.access_token),
        }
