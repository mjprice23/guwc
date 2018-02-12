from django.urls import path
from .views import BabyListView, BabyDetailView, BabyAddView


urlpatterns = [
    path('', BabyListView.as_view(), name='baby-list'),
    path('add/', BabyAddView.as_view(), name='baby-add'),
    path('<uuid:pk>/', BabyDetailView.as_view(), name='baby-detail'),
]