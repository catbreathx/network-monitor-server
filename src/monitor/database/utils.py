import json

import bcrypt
from sqlalchemy.orm import DeclarativeMeta


class PasswordHash(object):
    def __init__(self, password_hash: str):
        password_has_bytes = password_hash.encode("utf-8")
        assert len(password_has_bytes) == 60, "bcrypt hash should be 60 chars."
        assert password_has_bytes.count(b"$"), 'bcrypt hash should have 3x "$".'
        self.hash = password_has_bytes
        self.rounds = int(self.hash.split(b"$")[2])

    def __eq__(self, password):
        result = False

        if isinstance(password, str):
            candidate = password.encode("utf-8")
            result = bcrypt.checkpw(candidate, self.hash)

        return result

    def __repr__(self):
        """Simple object representation."""
        return "<{}>".format(type(self).__name__)

    @classmethod
    def new(cls, password, rounds):
        if isinstance(password, str):
            password = password.encode("utf-8")

        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(rounds))

        instance = cls(hashed_password.decode("utf-8"))
        return instance


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith("_") and x != "metadata"]:
                if field in ["registry"]:
                    continue

                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


def model_list_to_json(models: list) -> list[dict]:
    result = [model.json() for model in models]
    return result
