from django.http import HttpRequest, JsonResponse
from .themovidb import TheMovieDb
from .models import TvShow

def index(request: HttpRequest) -> JsonResponse:
    movie_api = TheMovieDb()
    search_query = request.GET.get("query")
    if search_query is None:
        return JsonResponse({
            "status": "500",
            "message": "query parameter cannot be empty"
        })
    
    shows = TvShow.get_matching_shows(search_query)
    
    if len(shows) < 1:
        response = movie_api.search(search_query)
        shows = TvShow.insert_shows_from_api_response(response=response)

    return JsonResponse({
        "status": "200",
        "message": shows
    })
