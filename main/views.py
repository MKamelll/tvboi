from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def dashboard(request: HttpRequest) -> HttpResponse:
    context = {
        "items": [
            {
                "title": "fuck off",
                "action": "View Details"
            }
        ]
    }
    return render(request=request, template_name="main/dashboard.html", context=context)

def tvshow(request: HttpRequest) -> HttpResponse:
    context: dict[str, str | list[str]] = {
        "title": "Breaking Bad",
        "img_src": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTOcWkpWG_NRrU2M8-WB8EbEcJk7smhdrY1eO0ttKXm0bo2ooOEWxk3zBSbsFrSgSJh2OEKOQ",
        "summary": "A chemistry teacher diagnosed with inoperable lung cancer turns to manufacturing and selling methamphetamine with a former student to secure his family's future.",
        "cast": [
            "Bryan Cranston", "Anna Gunn", "Aaron Paul", "Dean Norris", "Betsy Brandt", "RJ Mitte", "Giancarlo Esposito"
        ]
    }
    return render(request=request, template_name="main/tvshow.html", context=context)