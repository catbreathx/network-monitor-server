from .base import BaseHotasModel
from .host import Host, HostCreate, HostCreateOut, HostUpdate
from .host_health_check import HostHealthCheckIn, HostHealthCheckOut
from .login import Credentials
from .password_validator import PasswordValidator
from .scheduled_job import ScheduledJobCreate, ScheduledJobOut
from .user import User, UserCreate, UserCreateOut, UserGetOut, UserUpdate


def init_schema(app):
    BaseHotasModel.init_app(app)
