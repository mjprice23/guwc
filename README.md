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

## Making our Students App (chkpt2)
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

### Admin Interface (chkpt2)
* Django provides a really nice built-in admin interface to interact
with our data models.  It is easy to implement, and usable in production
code.
* In our `admin.py` file, let's put the following code:
```python
from django.contrib import admin
from .models import MagicalBaby


class MagicalBabyAdmin(admin.ModelAdmin):
    pass

admin.site.register(MagicalBaby, MagicalBabyAdmin)
```

* There is a LOT of automagic going on here, but essentially what we
are doing is allowing admin users to see, edit, add, and delete any
records of the Student model that exist in our database.
* Our only problem is that we don't currently have an admin user.
To remedy this, let's type: `./manage.py createsuperuser` and fill in
the information it asks you for.
* Let's take a look at the admin interface. Type in
`./manage.py runserver` and in your web browser, navigate to
`127.0.0.1:8000/admin`. Type in the credentials of the admin user
you just created.
* When you've logged in, you should see something like this:

    ![admin_interface]
* Click on `Magical babys` and then click `Add Student` in the top right
corner of the whitespace.  We should then see an interface to add a
student, like this:

    ![add_student]

* Let's add a student for each house.  After you've added them, the
student list should look similar to this:

    ![student_list]

* We can delete or edit any of these students, if we so choose, by
clicking on their name in the list above.

* This admin interface is not the prettiest by any means, but it is
indeed functional, and is perfectly acceptable for use in production.

* We will now move on to the middleware, creating a view, and a form for
editing and adding students.

[admin_interface]: images/admin_interface.png
[add_student]: images/add_student.png
[student_list]: images/student_list.png

