from fastapi import FastAPI
from pydantic import BaseModel


class Links(dict):
    # links: Optional[create_model('')
    pass


class BaseHotasModel(BaseModel):
    __fast_api_app = None

    @classmethod
    def init_app(cls, app: FastAPI):
        cls.__fast_api_app = app
