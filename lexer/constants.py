class Constants:
    CONSTANTS = {
        'PI' : 3.14,
        'E' : 2.78,
        'GR' : 1.618
    }

    def isExists(self, key):
        return False if self.CONSTANTS.get(key) is None else True

    def get(self, key):
        return self.CONSTANTS.get(key, 0)