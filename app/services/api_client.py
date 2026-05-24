import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from flask import current_app


class APIClient:
    def __init__(self):
        self.session = requests.Session()
        retry = Retry(
            total=current_app.config["MAX_RETRIES"],
            backoff_factor=0.3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retry))

    def get_json(self, url, params=None):
        response = self.session.get(url, params=params, timeout=current_app.config["REQUEST_TIMEOUT"])
        response.raise_for_status()
        return response.json()
