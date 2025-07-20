from rest_framework import serializers
from .models import TvShow, TvSeason, Episode

class TvshowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TvShow
        fields = "__all__"

class TvSeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TvSeason
        fields = "__all__"

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = "__all__"