class Variables:
    VARIABLES = {}

    def is_exists(self, key):
        return False if self.VARIABLES.get(key) is None else True

    def get(self, key):
        return self.VARIABLES.get(key, 0)

    def add(self, key, value):
        type, name = key.split(' ')
        self.VARIABLES[name] = {
            'type': type,
            'value': value
        }

variables = Variables()