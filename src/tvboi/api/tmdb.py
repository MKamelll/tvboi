import httpx
import os
from pydantic import BaseModel, ValidationError
from .pydantic_models import (
    SearchResults,
    Show,
    Season,
    Episode,
    CrewMember,
    GuestStar,
    Failure,
)


class TmdbException(Exception):
    pass


class TmdbResponseException(TmdbException):
    def __init__(self, status_code: int, status_message: str) -> None:
        super().__init__()
        self.status_code = status_code
        self.status_message = status_message


class Api:
    def __init__(self) -> None:
        self.api_key = os.getenv("api_key")
        self.api_access_token = os.getenv("api_access_token")
        self.base_url = "https://api.themoviedb.org/3"

    def get[T: BaseModel](
        self,
        endpoint: str,
        model: type[T],
        params: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
    ) -> T:
        if not headers:
            headers = {}
        if not params:
            params = {}
        if self.api_access_token is None or self.api_key is None:
            raise TmdbException("no credentials")
        headers["accept"] = "application/json"
        headers["Authorization"] = "Bearer " + self.api_access_token
        res = httpx.get(self.base_url + endpoint, params=params, headers=headers)
        res_json = res.json()
        if not res.is_success:
            try:
                fail = Failure.model_validate(res_json)
                raise TmdbResponseException(
                    status_code=fail.status_code, status_message=fail.status_message
                )
            except ValidationError as e:
                raise TmdbResponseException(status_code=500, status_message=str(e))
        return model.model_validate(res_json)

    def search_for_show(self, query: str) -> SearchResults:
        return self.get("/search/tv", params={"query": query}, model=SearchResults)

    def get_show_details(self, series_id: int) -> Show:
        return self.get(f"/tv/{series_id}", model=Show)

    def get_season_details(self, series_id: int, season_number: int) -> Season:
        return self.get(f"/tv/{series_id}/season/{season_number}", model=Season)

    def get_episode_details(
        self, series_id: int, season_number: int, episode_number: int
    ) -> Episode:
        return self.get(
            f"/tv/{series_id}/season/{season_number}/episode/{episode_number}",
            model=Episode,
        )


api = Api()
