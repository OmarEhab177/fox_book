from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from verified_email_field.models import VerifiedEmailField

from .managers import CustomUserManager
# from core.models import Plan

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    fullname = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    image = models.ImageField(upload_to = 'photos/users/%y/%m/%d')
    code = models.TextField()
    remember_token = models.TextField()
    is_pan = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [phone, fullname]

    objects = CustomUserManager()

    def __str__(self):
        return self.email