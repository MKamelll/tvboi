from dotenv import load_dotenv
import httpx
import os
from typing import Any
load_dotenv()

class TheMovieDb:
    def __init__(self) -> None:
        self.access_token = os.getenv("api_access_token") or ""
        assert self.access_token != "", "access token is missing"
        self.api_key = os.getenv("api_key") or ""
        assert self.api_key != "", "api key is missing"
        self.base_url = "https://api.themoviedb.org/3"
    
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