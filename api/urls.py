from django.urls import path
from . import views

urlpatterns = [
    path('search/<slug:slug>', view=views.search, name='search'),
    path('details/<int:id>', view=views.details, name='details')
]