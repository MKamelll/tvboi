import httpx
import os
from pydantic import BaseModel
from .pydantic_models import (
    SearchResults,
    Show,
    Season,
    Episode,
    CrewMember,
    GuestStar,
    Failure,
    Success,
)


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
    ) -> Success[T] | Failure:
        if not headers:
            headers = {}
        if not params:
            params = {}
        if self.api_access_token is None or self.api_key is None:
            return Failure(status_code=500, status_message="missing credentials")
        headers["accept"] = "application/json"
        headers["Authorization"] = "Bearer " + self.api_access_token
        res = httpx.get(self.base_url + endpoint, params=params, headers=headers)
        res_json = res.json()
        if not res.is_success:
            return Failure(
                status_code=res_json["status_code"],
                status_message=res_json["status_message"],
            )
        return Success(data=model.model_validate(res_json))

    def search_for_show(self, query: str) -> Success[SearchResults] | Failure:
        return self.get("/search/tv", params={"query": query}, model=SearchResults)

    def get_show_details(self, series_id: int) -> Success[Show] | Failure:
        return self.get(f"/tv/{series_id}", model=Show)

    def get_season_details(
        self, series_id: int, season_number: int
    ) -> Success[Season] | Failure:
        return self.get(f"/tv/{series_id}/season/{season_number}", model=Season)

    def get_episode_details(
        self, series_id: int, season_number: int, episode_number: int
    ) -> Success[Episode] | Failure:
        return self.get(
            f"/tv/{series_id}/season/{season_number}/episode/{episode_number}",
            model=Episode,
        )


api = Api()
