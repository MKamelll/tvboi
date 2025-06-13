from django.http import HttpRequest, JsonResponse
from dotenv import load_dotenv
import os
import httpx
from .models import TvShow
load_dotenv()

base_url = "https://api.themoviedb.org/3"

def index(request: HttpRequest) -> JsonResponse:
    access_token = os.getenv("api_access_token")
    assert(access_token is not None)
    headers = {
        "Authorization": "Bearer " + access_token,
        "accept": "application/json"
    }
    parameters = {
        "include_adult": "true",
        "language": "en-US",
        "page": "1",
        "query": "breaking bad"
    }
    response = httpx.get(base_url + "/search/tv", headers=headers, params=parameters).json()

    shows: list[TvShow] = []

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
