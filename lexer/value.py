class Value:
    def as_integer(self):
        raise NotImplementedError

    def as_string(self):
        raise NotImplementedError


class NumberValue(Value):
    def __init__(self, value):
        self.value = value

    def as_integer(self):
        return self.value

    def as_string(self):
        return str(self.value)


class StringValue(Value):
    def __init__(self, value):
        self.value = value

    def as_integer(self):
        return int(self.value)

    def as_string(self):
        return self.value