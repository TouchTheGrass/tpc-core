from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class ThreeChessUserManager(BaseUserManager):
    def create_user(self, username=None, email=None, password=None):
        if username is None:
            raise ValueError('Users mush have a username.')
        if email is None:
            raise ValueError('Users mush have an email address.')
        if password is None:
            raise ValueError('Users mush have a password.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username=username, email=email, password=password)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class ThreeChessUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        db_index=True,
        max_length=400,
        unique=True,
        error_messages={'unique': 'User with this username already exists.'},
    )
    email = models.EmailField(
        db_index=True,
        unique=True,
        error_messages={'unique': 'User with this email already exists.'},
    )
    scores = models.IntegerField(default=0)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = ThreeChessUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
