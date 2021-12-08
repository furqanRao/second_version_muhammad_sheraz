from django.db import models
from django.contrib.auth.models import User
from datetime import date


gender_choices = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=100, choices=gender_choices, default="Male")
    country = models.CharField(max_length=100, blank=True, default="UK")
    city = models.CharField(max_length=100, blank=True, default="LONDON")

    def __str__(self):
        return self.user.username


class ProductData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    product = models.CharField(max_length=255, default="")
    sales_number = models.IntegerField(default=0)
    revenue = models.DecimalField(default=0, null=True, max_digits=19, decimal_places=2)
    date = models.CharField(max_length=55, default="")

    def __str__(self):
        return self.product


class Country(models.Model):
    name = models.CharField(max_length=255, default="UK", unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, related_name='cities', on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=255, default="LONDON", unique=True)

    def __str__(self):
        return self.name
