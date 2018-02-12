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
        default=1997,
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
* Click on `Magical babys` and then click `Add Magical Baby` in the top right
corner of the whitespace.  We should then see an interface to add a
baby, like this:

    ![add_baby]

* Let's add a couple of babies.  After you've added them, the
baby list should look similar to this:

    ![baby_list]

* We can delete or edit any of these babies, if we so choose, by
clicking on their name in the list above.

* This admin interface is not the prettiest by any means, but it is
indeed functional, and is perfectly acceptable for use in production.

* We will now move on to the middleware, creating a view, and a form for
editing and adding babies.

[admin_interface]: images/admin_interface.png
[add_baby]: images/add_baby.png
[baby_list]: images/baby_list.png

### Creating Views and Connecting them with URLs (chkpt3)
Obviously, not everyone should have admin powers on our site, and we
want others to be able to come and register students.  To do that, we
need to create views to prepare and serve web pages.

* We want to display the list of students who go to Hogwarts, as well
as see specific student details.  Finally, we want to be able to add
students to our list.  For this, we will use three separate views, a
list view, a detail view where we can view and edit student information,
and a view for adding students.

* First, we will create a list view.  In `views.py`:
```python
from django.views.generic.list import ListView
from .models import MagicalBaby


class BabyListView(ListView):

    model = MagicalBaby

```

* There is a lot of automagic stuff going on here, but we still have
to string this view to a URL.  Let's create a `urls.py` file in the
`students/` directory.  In it, we will put the following:
```python
from django.urls import path
from .views import BabyListView


urlpatterns = [
    path('', BabyListView.as_view(), name='baby-list'),
]
```

* This is *almost* enough.  Django does not automagically know that this
URL configuration exists, so we must string it through to the URL file
that is acknowledges, which is in the `hogwarts/` directory.  In
`hogwarts/urls.py`, let's put:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('students/', include('students.urls')),
]
```

* This tells Django that whenever we see a URL that begins with
`students/`, we should refer to the URLs defined in the students app.
This is useful, because we can set up the students module to work on its
own, and then plug it into any larger Django project, just by adding
it to the settings.py and including its URL config in the main
`urls.py`.  Nifty.

* Another automagic part of the `ListView` that we used for our view is
an implied html file.  Because we set `model = MagicalBaby`, Django will
search for an html file named `[model_name]_list.html`, in this case,
`magicalbaby_list.html`.  Specifically, it will search in
`[app_name]/templates/[app_name]/` for that file.  Let's make that path
for Django by typing into the command line:
```
mkdir templates
cd templates
mkdir students
cd students
touch magicalbaby_list.html
```

* We now have the correct path with a blank html file.  Back in the IDE,
 add the following to the `magicalbaby_list.html` file:
 ```html
<ul>
{% for baby in object_list %}
    <li>{{ baby.first_name }} {{ baby.last_name }}, {{ baby.birth_year }}, {{ baby.get_dad_house_display }}, {{ baby.get_mom_house_display }}</li>
{% endfor %}
</ul>
 ```

* This code above is jinja2 template code.  The `object_list` is data
that is automatically passed through the `ListView` to the template. It
is accessible only through the template at the point at which the page
loads.  We take advantage of this passed-through data to display our
list of students.

* Back in the main `hogwarts/` directory, let's run our server again.
Enter `./manage.py runserver`, and in your web browser, navigate to
`127.0.0.1:8000/students/`.  You should see a list of the Hogwarts
students that we created in our admin interface.

* We would like to be able to edit the information of each student, so
let's now make a view for that. Thankfully, Django has us automagically
covered. It has a built-in `UpdateView` and `CreateView` for just this
occasion. Let's change our `views.py` to the following:
```python
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from .models import MagicalBaby


class BabyListView(ListView):

    model = MagicalBaby


class BabyDetailView(UpdateView):

    model = MagicalBaby
    fields = '__all__'
    template_name = 'students/baby_form.html'
    success_url = reverse_lazy('baby-list')


class BabyAddView(CreateView):

    model = MagicalBaby
    fields = '__all__'
    template_name = 'students/baby_form.html'
    success_url = reverse_lazy('baby-list')
```

* Notice two things here:
    * `template_name` is the same in both views.  This is because the
    actual form underlying the two views is the same, so we only need
    to make one html template.
    * `success_url` redirects to the `reverse_lazy('baby-list')`.
    What's happening here is actually simple.  `reverse` means we are
    asking Django to reverse-engineer what URL to redirect to based on
    the name we gave it. In this case, we are asking it to redirect to
    the student list view.  The `lazy` tacked on to the function simply
    waits to calculate the exact URL until it is needed.

* We need to string these views to URLs, so we need to edit our
`students/urls.py` to add URLs for them:
```python
from django.urls import path
from .views import BabyListView, BabyDetailView, BabyAddView


urlpatterns = [
    path('', BabyListView.as_view(), name='baby-list'),
    path('add/', BabyAddView.as_view(), name='baby-add'),
    path('<uuid:pk>/', BabyDetailView.as_view(), name='baby-detail'),
]
```

* The last path in the `urlpatterns` is a catch-all for UUIDs, which we
use as IDs for all of our students.  If we know that UUID for a student,
we can connect directly to the editor.  It would be unkind for us to
force people to remember the UUID of any student that they want to
look up, so we will edit the `magicalbaby_list.html` to add links to
each student's editing form:
```
<ul>
{% for baby in object_list %}
    <li><a href="{{ baby.id }}/">{{ baby.first_name }} {{ baby.last_name }}</a>, {{ baby.birth_year }}, {{ baby.get_dad_house_display }}, {{ baby.get_mom_house_display }}</li>
{% endfor %}
</ul>
```

* Finally, we need to create `magicalbaby_form.html` in the same
directory as `magicalbaby_list.html`, and add the following code to
make it work:
```
<form action="" method="post">
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Submit" />
</form>
```

* Because Django automagically creates the form for us, we just
need to call it in the html template.

* The site is now fully functional!  We can add new students, edit the
current students, and see our progress.  In the admin interface, we can
do all of that, and delete users.  There are many different directions
that we can go from here, like adding users as a layer of security so
that you need to log in if you want to add students. We could also
 add a sorting hat function so that if you create a first year,
 they will automatically be sorted into a house instead of giving you
the option of choosing the house.  The last thing that we will do
is attempt to make our website look nice, by adding some CSS and
structure.

### Making it look nice(ish) (chkpt4.1)
* Django makes it easy to add static content, in much the same way that
we added templates in prior sections. In our `students` directory, we
add a `static/students/` directory, and then add all of our static files
like CSS and images to that. In our html templates, we can use the
command `{% load staticfiles %}` to get access to our static files.
We can import them like this:
`<link rel="stylesheet" type="text/css" href="{% static 'students/css/base.css' %}"/>`

* We can reference images directly in our CSS files:
`background-image: url('../images/background.jpg');`

* We wanted bootstrap, and there is actually a Django package for
easy inclusion in your templates.  It is already installed in the
requirements, and we can add it to our `INSTALLED_APPS` in the
settings: `'bootstrap3',`.  In our templates, we import it like this:
```jinja2
{% load bootstrap3 %}
{% bootstrap_css %}
{% bootstrap_javascript jquery=1 %}
```

* The full guide on jinja2 is slightly out of the scope of this lesson,
but it is a pretty powerful, easy to learn templating framework. If you
plan on using Django, I would highly recommend learning it.

This is a very simple example of a Django application. Django supports
much more complicated models, operations, and applications. It also
supports one of the most robust API frameworks,
Django REST Framework (DRF). One thing that we did not touch during
this lesson is `tests`. Any time that you write production code in Django,
it is worthless unless it has good test coverage. Django makes tests
easy to implement, and there are many add-ons for creating succint,
replicable tests in Django.