from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    fullname = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15)
    
    SA = 1
    A = 2
    ROLE_CHOICES = (
        (SA, 'Super Admin'),
        (A,'Admin'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def getRoleName(self):
        if self.role==1:
            return 'Super Admin'
        elif self.role==2:
            return 'Admin'
        else:
            return 'None'
  