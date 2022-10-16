class ResourceNotFoundException(Exception):
    _resource_id: str
    _resource_type: str

    @property
    def resource_id(self):
        return self._resource_id

    @property
    def resource_type(self):
        return self._resource_type

    def __init__(self, resource_id, resource_type):
        super(ResourceNotFoundException, self).__init__()
        self._resource_id = resource_id
        self._resource_type = resource_type


class AuthenticationException(Exception):
    pass


class DuplicateUser(Exception):
    _email = None

    @property
    def email(self):
        return self._email

    def __init__(self, email: str) -> None:
        super().__init__()
        self._email = email

    def __str__(self) -> str:
        return f"User with {self._email} already exists"
