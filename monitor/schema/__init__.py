from .base import BaseHotasModel
from .credentials import Credentials
from .host import Host
from .host import HostCreate
from .user import PutUser
from .user import User
from .user import UserCreate


def init_schema(app):
    BaseHotasModel.init_app(app)
