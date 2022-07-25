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
