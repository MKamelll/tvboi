from rest_framework import serializers
from .models import TvShow, TvSeason

class TvshowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TvShow
        fields = "__all__"

class TvSeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TvSeason
        fields = "__all__"