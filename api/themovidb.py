from __future__ import annotations
from dotenv import load_dotenv
import httpx
import os
from typing import Any
load_dotenv()

class TheMovieDb:
    instance: TheMovieDb | None = None
    def __init__(self) -> None:
        self.access_token = os.getenv("api_access_token") or ""
        assert self.access_token != "", "access token is missing"
        self.api_key = os.getenv("api_key") or ""
        assert self.api_key != "", "api key is missing"
        self.base_url = "https://api.themoviedb.org/3"
    
    @staticmethod
    def get_instance() -> TheMovieDb:
        if TheMovieDb.instance is None:
            TheMovieDb.instance = TheMovieDb()
            return TheMovieDb.instance
        return TheMovieDb.instance
    
    def make_request(self, endpoint:  str, params: dict[str, str]={}) -> Any:
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "accept": "application/json"
        }
        response = httpx.get(self.base_url + endpoint, headers=headers, params=params).json()
        return response

    def search(self, query: str) -> Any:
        return self.make_request("/search/tv", params={"query": query})
    
    def details(self, show_id: int) -> Any:
        return self.make_request(f"/tv/{show_id}")
    
    def season(self, show_id: int, season_number: int) -> Any:
        return self.make_request(f"/tv/{show_id}/season/{season_number}")
    
    def episode(self, show_id: int, season_number: int, episode_number: int) -> Any:
        return self.make_request(f"/tv/{show_id}/season/{season_number}/episode/{episode_number}")