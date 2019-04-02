class Variables:
    VARIABLES = {}

    def isExists(self, key):
        return False if self.VARIABLES.get(key) is None else True

    def get(self, key):
        return self.VARIABLES.get(key, 0)

    def add(self, key, value):
        self.VARIABLES[key] = value

variables = Variables()