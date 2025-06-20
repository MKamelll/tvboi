from __future__ import annotations
from django.db import models
from typing import Any

class TvShow(models.Model):
    id: models.CharField[str, str] = models.CharField(max_length=10, unique=True, primary_key=True)
    origin_country: models.CharField[str, str | None] = models.CharField(null=True, max_length=20)
    original_language: models.CharField[str, str | None] = models.CharField(null=True, max_length=20)
    name: models.CharField[str, str | None] = models.CharField(null=True, max_length=50)
    overview: models.TextField[str, str | None] = models.TextField(null=True)
    poster_path: models.URLField[str, str | None] = models.URLField(null=True)
    first_air_date: models.CharField[str, str | None] = models.CharField(null=True, max_length=50)
    vote_average: models.IntegerField[str, int | None] = models.IntegerField(null=True)

    @staticmethod
    def is_tvshow_already_available(tvshow_name: str | None) -> bool:
        return TvShow.objects.filter(name=tvshow_name).exists()
    
    @staticmethod
    def insert_shows_from_api_response(response: Any) -> list[TvShow]:
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
            if not TvShow.is_tvshow_already_available(show.name):
                shows.append(show)

        TvShow.objects.bulk_create(shows)
        
        return shows
