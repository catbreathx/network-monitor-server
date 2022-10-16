import json

from pydantic import BaseModel
from requests import Response


def get_access_token(response: Response) -> str:
    json = response.json()
    access_token = json["access_token"]

    return access_token


def assert_model_response(schema_model: BaseModel, response_model: dict) -> None:
    assert_response_model = response_model.copy()
    del assert_response_model["id"]

    normalized_schema_model = json.loads(schema_model.json())
    assert normalized_schema_model == assert_response_model


def assert_success_response_with_id(
    response: Response, expected_status_code, expected_resource_id: int
):
    assert response.status_code == expected_status_code
    host_response = response.json()
    assert host_response["id"] == expected_resource_id
