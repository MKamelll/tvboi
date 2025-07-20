from django.urls import path
from . import views

urlpatterns = [
    path('search/<slug:slug>', view=views.search, name='search'),
    path('details/<int:id>', view=views.details, name='details'),
    path('details/<int:show_id>/season/<int:season_number>', view=views.season, name='season')
]