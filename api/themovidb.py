from dotenv import load_dotenv
import httpx
import os
from typing import Any
load_dotenv()

class TheMovieDb:
    def __init__(self) -> None:
        self.access_token = os.getenv("api_access_token") or ""
        assert(self.access_token != "")
        self.api_key = os.getenv("api_key") or ""
        assert(self.api_key != "")
        self.base_url = "https://api.themoviedb.org/3"

    def search(self, query: str) -> Any:
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "accept": "application/json"
        }
        parameters = {
            "include_adult": "true",
            "language": "en-US",
            "page": "1",
            "query": query
        }
        response = httpx.get(self.base_url + "/search/tv", headers=headers, params=parameters).json()
        return response