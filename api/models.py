from __future__ import annotations
from django.db import models

class TvShow(models.Model):
    id = models.CharField(unique=True, primary_key=True)
    origin_country = models.CharField(null=True)
    original_language = models.CharField(null=True)
    name = models.CharField(null=False, default="Untitled Show")
    slug = models.SlugField(null=True)
    overview = models.TextField(null=True)
    poster_path = models.URLField(null=True)
    first_air_date = models.CharField(null=True)
    vote_average = models.IntegerField(null=True)