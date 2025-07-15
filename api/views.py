from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from .themovidb import TheMovieDb
from .models import TvShow
from .serializers import TvshowSerializer
from django.utils.text import slugify

@api_view(["GET"])
def search(request: Request, slug: str) -> Response:
    show = TvShow.objects.filter(slug__icontains=slug).all()
    seriazlizer = TvshowSerializer(show, many=True)
    if len(show) > 0:
        return Response(seriazlizer.data)
    
    api = TheMovieDb()
    results = api.search(slug)
    new_shows = []
    shows = []
    for i in results["results"]:
        search_res = TvShow()
        search_res.id = i["id"]
        search_res.name = i["name"]
        search_res.origin_country = i["origin_country"][0]
        search_res.overview = i["overview"]
        search_res.poster_path = i["poster_path"]
        search_res.vote_average = i["vote_average"]
        search_res.slug = slugify(i["name"])
        search_res.original_language = i["original_language"]
        search_res.first_air_date = i["first_air_date"]

        if not TvShow.objects.filter(id=search_res.id).exists():
            new_shows.append(search_res)
        else:
            shows.append(search_res)
    
    TvShow.objects.bulk_create(new_shows)
    seriazlizer = TvshowSerializer([*shows, *new_shows], many=True)
    return Response(seriazlizer.data)


@api_view(["GET"])
def details(request: Request, id: int) -> Response:
    show = TvShow.objects.filter(id=id).first()
    if show:
        are_show_details_full = True
        sz = TvshowSerializer(show)
        for value in sz.data.values():
            if not value:
                are_show_details_full = False
                break
        if are_show_details_full:
            return Response(sz.data)

    api = TheMovieDb()
    show_details = api.details(id)
    if show:
        for key, value in sz.data.items():
            if not value:
                setattr(show, key, show_details[key])
        show.save()
        sz = TvshowSerializer(show)
        return Response(sz.data)
    
    new_show = TvShow()
    new_show.id = show_details["id"]
    new_show.name = show_details["name"]
    new_show.overview = show_details["overview"]
    new_show.vote_average = show_details["vote_average"]
    new_show.slug = slugify(show_details["name"])
    new_show.origin_country = show_details["origin_country"]
    new_show.poster_path = show_details["poster_path"]
    new_show.number_of_seasons = show_details["number_of_seasons"]
    new_show.number_of_episodes = show_details["number_of_episodes"]
    new_show.save()

    sz = TvshowSerializer(new_show)
    return Response(sz.data)