from django.db import models

class TvShow(models.Model):
    id: models.CharField[str, str] = models.CharField(max_length=10, unique=True, primary_key=True)
    origin_country: models.CharField[str, str | None] = models.CharField(null=True, max_length=20)
    original_language: models.CharField[str, str | None] = models.CharField(null=True, max_length=20)
    name: models.CharField[str, str | None] = models.CharField(null=True, max_length=50)
    overview: models.TextField[str, str | None] = models.TextField(null=True)
    poster_path: models.URLField[str, str | None] = models.URLField(null=True)
    first_air_date: models.CharField[str, str | None] = models.CharField(null=True, max_length=50)
    vote_average: models.IntegerField[str, int | None] = models.IntegerField(null=True)