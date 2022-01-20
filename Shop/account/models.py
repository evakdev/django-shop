from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER_CHOICES = [("F", "Female"), ("M", "Male"), ("U", "Prefer Not to Say")]
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['password1','password2']
    @property
    def full_name(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"
