from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser


class UserProfile(AbstractBaseUser):
    """main user model"""
    phone_number = models.CharField(max_length=15, unique=True)
    auth_code = models.CharField(max_length=4, null=True, blank=True)
    referral_code = models.CharField(max_length=6, unique=True, null=True)
    used_referral_code = models.ForeignKey('self', on_delete=models.CASCADE,
                                           null=True, blank=True)
    password = models.CharField(
        max_length=128, default=None, blank=True, null=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.phone_number
 