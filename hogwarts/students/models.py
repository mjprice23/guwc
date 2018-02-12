from django.db import models
import uuid
from django_extensions.db.models import TimeStampedModel
from django.core.validators import MaxValueValidator, MinValueValidator
import logging


log = logging.getLogger(__name__)

class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True


class TimeStampedUUIDModel(TimeStampedModel, UUIDModel):

    class Meta:
        abstract = True


class MagicalBaby(TimeStampedUUIDModel):
    GRYFFINDOR = 'GR'
    SLYTHERIN = 'SL'
    RAVENCLAW = 'RA'
    HUFFLEPUFF = 'HU'
    NONE = 'NO'
    HOUSE_CHOICES = (
        (GRYFFINDOR, 'Gryffindor'),
        (SLYTHERIN, 'Slytherin'),
        (RAVENCLAW, 'Ravenclaw'),
        (HUFFLEPUFF, 'Hufflepuff'),
        (NONE, 'None'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dad_house = models.CharField(
        max_length=2,
        choices=HOUSE_CHOICES,
        default=NONE,
    )
    mom_house = models.CharField(
        max_length=2,
        choices=HOUSE_CHOICES,
        default=NONE,
    )
    birth_year = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(2018),
            MinValueValidator(1900),
        ]
    )

    class Meta:
        ordering = ['birth_year', 'last_name', 'first_name', 'dad_house', 'mom_house']

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name, self.birth_year, self.dad_house, self.mom_house)


class Student(TimeStampedUUIDModel):
    GRYFFINDOR = 'GR'
    SLYTHERIN = 'SL'
    RAVENCLAW = 'RA'
    HUFFLEPUFF = 'HU'
    HOUSE_CHOICES = (
        (GRYFFINDOR, 'Gryffindor'),
        (SLYTHERIN, 'Slytherin'),
        (RAVENCLAW, 'Ravenclaw'),
        (HUFFLEPUFF, 'Hufflepuff'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    house = models.CharField(
        max_length=2,
        choices=HOUSE_CHOICES,
        default=HUFFLEPUFF,
    )
    year = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(7),
            MinValueValidator(1),
        ]
    )

    class Meta:
        ordering = ['house', 'last_name', 'first_name']

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name, self.house, self.year)