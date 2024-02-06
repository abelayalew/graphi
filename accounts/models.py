import random

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone

from lib.mixins.models import NULL, BaseModelMixin


def generate_otp():
    return "".join([str(random.randint(0, 9)) for _ in range(6)])


class UserManager(BaseUserManager):
    def create(self, password=None, **kwargs):
        if kwargs.get("password"):
            password = kwargs.pop("password")

        user = self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, password, **kwargs):
        kwargs["is_staff"] = True
        kwargs["is_superuser"] = True

        return self.create(password=password, **kwargs)

    def create_user(self, password=None, **kwargs):
        kwargs["is_staff"] = False
        kwargs["is_superuser"] = False

        return self.create(password=password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)

    date_joined = models.DateTimeField(default=timezone.localtime, editable=False)
    last_login = models.DateTimeField(**NULL)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]

    objects = UserManager()
    graphql_exclude_fields = ("password",)

    def __str__(self):
        return self.email


class OTP(BaseModelMixin):
    user = models.ForeignKey(User, models.CASCADE)
    otp = models.CharField(max_length=6, default=generate_otp)
    is_used = models.BooleanField(default=False)
    graphql_exclude = False

    def __str__(self):
        return self.otp

class Employee(BaseModelMixin):
    user = models.ForeignKey(User, models.CASCADE)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    salary = models.IntegerField()
    designation = models.CharField(max_length=50)

    graphql_permissions = ["add_employee"]

    def __str__(self):
        return self.name