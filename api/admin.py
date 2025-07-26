from django.contrib import admin
from .models import TvShow, TvSeason, Episode, CrewMember, Guest, WatchedEpisode, WatchList

@admin.register(TvShow)
class TvShowAdmin(admin.ModelAdmin[TvShow]):
    pass

@admin.register(TvSeason)
class TvSeasonAdmin(admin.ModelAdmin[TvSeason]):
    pass

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin[Episode]):
    pass

@admin.register(CrewMember)
class CrewMemberAdmin(admin.ModelAdmin[CrewMember]):
    pass

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin[Guest]):
    pass

@admin.register(WatchedEpisode)
class WatchedEpisodeAdmin(admin.ModelAdmin[WatchedEpisode]):
    pass

@admin.register(WatchList)
class WatchListAdmin(admin.ModelAdmin[WatchList]):
    pass
