from requests import Response


def get_access_token(response: Response) -> str:
    json = response.json()
    access_token = json["access_token"]

    return access_token
