from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    GENDER_CHOICES = (
        ('M', 'Erkak'),
        ('F', 'Ayol'),
    )
    ACCESS = (
    (0, 'no_access'),
    (1, 'first_second'),
    (2, 'trird'),
    (4, 'all')
    )
    LANGUAGE_CHOICES = (
        ('uzbek', 'uzbek'),
        ('russian', 'russian'),
    )
    COUNTRY_CHOICES = (
        ('Uzbekistan', 'Uzbekistan'),
        ('Qozogiston', 'Qozogiston'),
        ('Qirgiziston', 'Qirgiziston'),
        ('Tojikiston', 'Tojikiston'),
        ('Rossiya', 'Rossiya'),
        ('America', 'America'),
        ('Arab Amirligi', 'Arab Amirligi'),
        ('Boshqa davlat', 'Boshqa davlat'),
    )
    country = models.CharField(max_length=32, choices=COUNTRY_CHOICES)
    phone_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    test_access = models.IntegerField(choices=ACCESS, default=0)
    certificate = models.BooleanField(default=False)
    passed = models.BooleanField(default=False)
    language = models.CharField(max_length=32, choices=LANGUAGE_CHOICES, default="uzbek")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
