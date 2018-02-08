from django import forms
from .models import Student
from django.core.validators import MaxValueValidator, MinValueValidator


class StudentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    house = forms.CharField(
        max_length=2,
        widget=forms.Select(choices=Student.HOUSE_CHOICES)
    )
    year = forms.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(7),
            MinValueValidator(1),
        ]
    )

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'house', 'year']