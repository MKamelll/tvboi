from django.urls import path
from . import views

urlpatterns = [
    path('tvshow/', view=views.tvshow, name='tvshow'),
    path('', view=views.dashboard, name='dashboard'),
]
