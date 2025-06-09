from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="main/dashboard.html")

def tvshow(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="main/tvshow.html")