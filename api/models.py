from __future__ import annotations
from django.db import models

class TvShow(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    origin_country = models.CharField(null=True)
    original_language = models.CharField(null=True)
    name = models.CharField(null=False, default="Untitled Show")
    slug = models.SlugField(null=True)
    overview = models.TextField(null=True)
    poster_path = models.URLField(null=True)
    first_air_date = models.CharField(null=True)
    vote_average = models.IntegerField(null=True)
    number_of_seasons = models.IntegerField(null=True)
    number_of_episodes = models.IntegerField(null=True)

class TvSeason(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    overview = models.TextField(null=True)
    name = models.CharField(null=True)
    poster_path = models.CharField(null=True)
    season_number = models.IntegerField()
    vote_average = models.IntegerField()
    show = models.ForeignKey(to=TvShow, on_delete=models.CASCADE, related_name="seasons")

class CrewMember(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    department = models.CharField()
    job = models.CharField()
    credit_id = models.CharField()
    name = models.CharField()
    profile_path = models.CharField()

class Guest(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    character = models.CharField()
    name = models.CharField()
    profile_path = models.CharField()

class Episode(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    overview = models.TextField(null=True)
    name = models.CharField(null=True)
    season_number = models.IntegerField()
    episode_number = models.IntegerField()
    crewmembers = models.ManyToManyField(to=CrewMember, related_name="episodes")
    guests = models.ManyToManyField(to=Guest, related_name="episodes")
    season = models.ForeignKey(to=TvSeason, on_delete=models.CASCADE, related_name="episodes")
