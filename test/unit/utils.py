import json

from sqlalchemy.orm import DeclarativeMeta

from monitor.database.db import Base


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


def model_list_to_json(models: list[Base]) -> list[dict]:
    result = [json.loads(json.dumps(model, cls=AlchemyEncoder)) for model in models]
    return result


def model_to_json(model: Base) -> list[dict]:
    result = json.loads(json.dumps(model, cls=AlchemyEncoder))
    return result
