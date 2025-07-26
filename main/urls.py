from django.urls import path
from . import views

urlpatterns = [
    path('tvshow/', view=views.tvshow, name='tvshow'),
    path('signup/', view=views.signup, name="signup"),
    path('login/', view=views.login, name='login'),
    path('', view=views.dashboard, name='dashboard'),
]
