from .base import BaseHotasModel
from .host import Host
from .host import HostCreate


def init_schema(app):
    BaseHotasModel.init_app(app)
