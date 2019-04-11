from signals import output
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.polygon import Polygon


class Variables:
    VARIABLES = {}

    def is_exists(self, key):
        return False if self.VARIABLES.get(key) is None else True

    def get(self, key):
        return self.VARIABLES.get(key, 0)

    def add(self, key, value):
        if key in self.VARIABLES:
            self.VARIABLES[key]['value'] = value
        else:
            _type, name = key.split(' ')
            if _type == "figure" and not isinstance(value, (MultiPolygon, Polygon)) or \
                 _type in ('str', 'int') and _type != value.__class__.__name__:

                output.send("Can't assign '{}' to variable of type '{}'. Inappropriate value for this type.".format(
                    value, _type
                ))
                return
            else:
                self.VARIABLES[name] = {
                    'type': _type,
                    'value': value
                }


variables = Variables()