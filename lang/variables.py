from re import findall
class Variables:
    VARIABLES = {}
    OBJECTS = {}

    def is_exists(self, key):
        return False if self.VARIABLES.get(key) is None else True

    def get(self, key):
        return self.VARIABLES.get(key, 0)

    def add(self, key, value):
        if key in self.VARIABLES:
            self.VARIABLES[key]['value'] = value
        else:
            type, name = key.split(' ')
            self.VARIABLES[name] = {
                'type': type,
                'value': value
            }
    
    def add_object(self, key, value):
        self.OBJECTS[key] = value

    def get_object(self, key):
        return self.OBJECTS[key]

variables = Variables()