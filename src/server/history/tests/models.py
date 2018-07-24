from common.models import TimeStampedUUIDModel
from django.db import models


class Person(TimeStampedUUIDModel):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    number_of_pets = models.IntegerField(default=0)

    class Meta:
        app_label = 'tests'
