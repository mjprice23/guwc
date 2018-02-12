from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from .models import Student, MagicalBaby


class BabyListView(ListView):

    model = MagicalBaby


class BabyDetailView(UpdateView):

    model = MagicalBaby
    fields = '__all__'
    template_name = 'students/magicalbaby_form.html'
    success_url = reverse_lazy('baby-list')


class BabyAddView(CreateView):

    model = MagicalBaby
    fields = '__all__'
    template_name = 'students/magicalbaby_form.html'
    success_url = reverse_lazy('baby-list')


class StudentListView(ListView):

    model = Student


class StudentDetailView(UpdateView):

    model = Student
    fields = '__all__'
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student-list')


class StudentAddView(CreateView):

    model = Student
    fields = '__all__'
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student-list')
