from requests import Request
from requests.auth import AuthBase


class JWTAuth(AuthBase):
    """Attaches HTTP Pizza Authentication to the given Request object."""

    def __init__(self, access_token: str):
        self.access_token = access_token

    def __call__(self, request: Request) -> Request:
        request.headers["Authorization"] = f"bearer {self.access_token}"
        return request
