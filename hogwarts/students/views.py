from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from .models import Student


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
