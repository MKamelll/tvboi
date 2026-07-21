from pydantic import BaseModel, field_validator


class CrewMember(BaseModel):
    id: int
    department: str
    job: str
    known_for_department: str
    name: str
    original_name: str
    profile_path: str | None = None


class GuestStar(BaseModel):
    id: int
    character: str
    known_for_department: str
    name: str
    original_name: str
    profile_path: str | None = None


class Episode(BaseModel):
    id: int
    episode_type: str
    episode_number: int
    name: str
    overview: str
    season_number: int
    show_id: int | None = None
    still_path: str | None = None
    vote_average: float
    vote_count: int
    crew: list[CrewMember] | None = None
    guests: list[GuestStar] | None = None

    @field_validator("still_path")
    @classmethod
    def build_still_path(cls, v: str | None) -> str | None:
        if v is None:
            return None
        return f"https://image.tmdb.org/t/p/w300{v}"


class SeasonBasic(BaseModel):
    id: int
    name: str
    overview: str
    poster_path: str | None = None
    season_number: int
    vote_average: float
    episode_count: int

    @field_validator("poster_path")
    @classmethod
    def build_poster_path(cls, v: str | None) -> str | None:
        if v is None:
            return None
        return f"https://image.tmdb.org/t/p/w300{v}"


class Season(SeasonBasic):
    episodes: list[Episode]


class ShowBasic(BaseModel):
    id: int
    origin_country: list[str]
    original_language: str
    original_name: str
    overview: str
    poster_path: str | None = None
    name: str
    first_air_date: str | None = None
    vote_average: float
    vote_count: int

    @field_validator("poster_path")
    @classmethod
    def build_poster_path(cls, v: str | None) -> str | None:
        if v is None:
            return None
        return f"https://image.tmdb.org/t/p/w300{v}"

    @field_validator("first_air_date")
    def build_year(cls, v: str | None) -> str | None:
        if v is None:
            return None
        year, month, day = v.split("-")
        return year


class Show(ShowBasic):
    number_of_episodes: int
    number_of_seasons: int
    seasons: list[SeasonBasic]


class SearchResults(BaseModel):
    page: int
    results: list[ShowBasic]


class Success[T](BaseModel):
    data: T


class Failure(BaseModel):
    status_code: int
    status_message: str
