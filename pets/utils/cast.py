from datetime import datetime

from pets import db
from pets.utils.consts import Consts


class Cast(object):
    @staticmethod
    def to_bool(val):
        if val is None:
            return False
        if isinstance(val, bool):
            return val
        return val.lower() in ["true", "1", "checked", "on"]

    @staticmethod
    def to_datetime(val):
        if not val:
            return None
        if isinstance(val, datetime):
            return val
        return datetime.strptime(val, Consts.DATE_FORMAT)

    @staticmethod
    def cast_to_col(val, col):
        if val == "":  # replace empty string with None
            return None
        if isinstance(col.type, db.Integer):
            return int(val)
        if isinstance(col.type, db.Float):
            return float(val)
        if isinstance(col.type, db.Boolean):
            return Cast.to_bool(val)
        if isinstance(col.type, db.Enum):
            for enum_val in col.type.python_type:
                # look for the right enum key
                if val == enum_val.name:
                    return enum_val
        if isinstance(col.type, db.DateTime):
            return datetime.strptime(val, Consts.DATE_FORMAT)
        # else: the col type is string
        return val
