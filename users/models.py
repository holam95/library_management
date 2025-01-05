from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class LibraryUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    date_of_membership = models.DateField(auto_now_add=True)
    active_status = models.BooleanField(default=True)
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username