## Professor McGonagall's List of Young Witches and Wizards
When Voldemort took over the Ministry of Magic in the summer of 1997, he
destroyed the register of magical babies, so parents have had to
manually sign their kids up for Hogwarts for the first time since
Rowena Ravenclaw created the register hundreds of years ago. Professor
McGonagall can't handle the peck of owls that have overrun the
circular headmistress's office, so we've been enlisted to create a
tool for parents to sign up their children online (McGonagall can go
somewhere less magical than Hogwarts to view the list during the summer).
We need to construct a web app to keep track of each child, the year that
they were born (starting September 1st, of course), and their parents'
houses while they were at Hogwarts.

## Requirements:
* Basic Knowledge of Python
* Python 3 installed
* Basic Knowledge of Command Line Interface

## Installing This Project:
* `git clone git@github.com:rchurch4/guwc.git`
* `cd guwc/`
* `pip install -r requirements.txt`

## Running This Project
* `./manage.py runserver`

## To Follow Along
* `git checkout start`

## Getting Started
* Your working directory should look like:
  ```
  LICENSE		hogwarts/
  README.md		requirements.txt
  ```
* `cd hogwarts`
* `./manage.py startapp students`
* Open the `hogwarts/` directory in your favorite IDE
* In `hogwarts/settings.py`, add the following to `INSTALLED_APPS`:
  ```
  'django_extensions',
  'students',
  ```

## Making our Students App (chkpt1)
* We will now work in the `students/` directory

### Models
* In `models.py`, we define the database models that we will use to
implement our students app
* We create base TimeStampedUUID Models to build our student model on:
```python
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
```

* We then create our MagicalBaby model to keep track of name, parents' houses, and birth year:

```python
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
```

* Back in the `hogwarts/` directory, on the command line, we will type:
`./manage.py makemigrations` to build the models we just made
* Once the migrations are built, we have to apply them to our database:
`./manage.py migrate`
    * Note: Django automagically creates us a default SQLite database.
    The settings.py file makes it easy to switch that out for any
    database we would like
* Once this is done, our models are ready to roll.  Next, we tackle the
admin interface, an easy way to mess with our backend.