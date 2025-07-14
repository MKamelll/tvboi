from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from .themovidb import TheMovieDb
from .models import TvShow
from .serializers import TvshowSerializer
from django.utils.text import slugify

@api_view(["GET"])
def search(request: Request, slug: str) -> Response:
    show = TvShow.objects.filter(slug__icontains=slug).first()
    seriazlizer = TvshowSerializer(show)
    if show:
        return Response(seriazlizer.data)
    
    api = TheMovieDb()
    results = api.search(slug)
    new_shows = []
    shows = []
    for i in results["results"]:
        show = TvShow()
        show.id = i["id"]
        show.name = i["name"]
        show.origin_country = i["origin_country"][0]
        show.overview = i["overview"]
        show.poster_path = i["poster_path"]
        show.vote_average = i["vote_average"]
        show.slug = slugify(i["name"])

        if not TvShow.objects.filter(id=show.id).exists():
            new_shows.append(show)
        else:
            shows.append(show)
    
    seriazlizer = TvshowSerializer([*shows, *new_shows], many=True)
    return Response(seriazlizer.data)


