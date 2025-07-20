from .models import TvSeason

def check_if_season_exists(show_id: int, season_number: int) -> TvSeason | None:
    return TvSeason.objects.filter(fk=show_id, season_number=season_number).first()