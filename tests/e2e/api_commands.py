import requests
from fastapi.encoders import jsonable_encoder
from requests import Response

from monitor import schema
from tests.e2e.request_utils import JWTAuth

BASE_URL = "http://localhost:5002/api/v1"


def create_user(user_create: schema.UserCreate, access_token: str) -> Response:
    json = jsonable_encoder(user_create.dict())
    response = requests.post(_get_url("/users"), json=json, auth=JWTAuth(access_token))

    return response


def create_host(host_create: schema.HostCreate, access_token: str) -> Response:
    json = jsonable_encoder(host_create.dict())
    response = requests.post(_get_url("/hosts"), json=json, auth=JWTAuth(access_token))

    return response


def update_host(resource_id: int, host_update: schema.HostUpdate, access_token: str) -> Response:
    json = jsonable_encoder(host_update.dict())
    response = requests.put(
        _get_url(f"/hosts/{resource_id}"), json=json, auth=JWTAuth(access_token)
    )

    return response


def get_one_host(resource_id: int, access_token: str) -> Response:
    response = requests.get(_get_url(f"/hosts/{resource_id}"), auth=JWTAuth(access_token))
    return response


def get_all_hosts(access_token: str) -> Response:
    response = requests.get(_get_url("/hosts"), auth=JWTAuth(access_token))
    return response


def run_health_check(access_token: str):
    response = requests.post(_get_url("/scheduledjob/ping"), auth=JWTAuth(access_token))
    return response


def _get_url(path: str) -> str:
    result = f"{BASE_URL}{path}"
    return result
