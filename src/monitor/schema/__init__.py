from .base import BaseHotasModel
from .host import Host
from .host import HostCreate
from .host import HostCreateOut
from .host import HostUpdate
from .login import Credentials
from .password_validator import PasswordValidator
from .user import PutUser
from .user import User
from .user import UserCreate
from .user import UserCreateOut
from .user import UserGetOut


def init_schema(app):
    BaseHotasModel.init_app(app)
