import requests
from fastapi.encoders import jsonable_encoder
from requests import Response

from e2e.request_utils import JWTAuth
from monitor import schema

BASE_URL = "http://localhost:5002/api/v1"


def login(email: str, password: str) -> Response:
    credentials = schema.Credentials(email=email, password=password)
    response = requests.post(_get_url("/login"), json=credentials.dict())

    return response


def create_user(user_create: schema.UserCreate, access_token: str) -> Response:
    json = jsonable_encoder(user_create.dict())
    response = requests.post(_get_url("/user"), json=json, auth=JWTAuth(access_token))

    return response


def create_host(host_create: schema.HostCreate, access_token: str) -> Response:
    json = jsonable_encoder(host_create.dict())
    response = requests.post(_get_url("/host"), json=json, auth=JWTAuth(access_token))

    return response


def _get_url(path: str) -> str:
    result = f"{BASE_URL}{path}"
    return result
