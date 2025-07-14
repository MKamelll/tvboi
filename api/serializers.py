from rest_framework import serializers
from .models import TvShow

class TvshowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TvShow
        fields = "__all__"

