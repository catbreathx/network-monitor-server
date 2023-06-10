import requests
from requests import Response

from monitor import schema
from tests.e2e import utils

BASE_URL = "http://localhost:5002/auth/v1"


def login(email: str, password: str) -> Response:
    credentials = schema.Credentials(email=email, password=password)
    response = requests.post(_get_url("/login"), json=credentials.dict())

    return response


def authenticate(email: str) -> str:
    response = login(email, "password")
    access_token = utils.get_access_token(response)

    return access_token


def _get_url(path: str) -> str:
    result = f"{BASE_URL}{path}"
    return result
