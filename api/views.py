from django.http import HttpRequest, JsonResponse
from .themovidb import TheMovieDb
from .models import TvShow

def index(request: HttpRequest) -> JsonResponse:
    movie_api = TheMovieDb()

    shows: list[TvShow] = []

    response = movie_api.search("Breaking bad")

    for result in response["results"]:
        show = TvShow()
        show.id = result["id"]
        show.origin_country = result["origin_country"]
        show.original_language = result["original_language"]
        show.name = result["name"]
        show.overview = result["overview"]
        show.poster_path = result["poster_path"]
        show.first_air_date = result["first_air_date"]
        show.vote_average = result["vote_average"]
        shows.append(show)
    
    TvShow.objects.bulk_create(shows)

    return JsonResponse({
        "status": "200"     
    })
