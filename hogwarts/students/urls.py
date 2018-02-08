from django.urls import path
from .views import StudentListView, StudentDetailView, StudentAddView


urlpatterns = [
    path('', StudentListView.as_view(), name='student-list'),
    path('add/', StudentAddView.as_view(), name='student-add'),
    path('<uuid:pk>/', StudentDetailView.as_view(), name='student-detail'),
]