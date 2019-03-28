from variables import *


class Expression:
    def evaluate(self):
        raise NotImplementedError


class NumberExpression(Expression):
    def __init__(self, number):
        self.number = number
    
    def __int__(self):
        return self.number

    def __str__(self):
        return "NumberExp({})".format(self.number)

    def __repr__(self):
        return self.__str__()


class ConstantExpression(Expression):
    def __init__(self, name):
        self.name = name

    def evaluate(self):
        vars = Variables()
        result = vars.get(self.name)
        if result is 0: 
            raise NameError("Constant doesn't exist")
        else: 
            return result

    def __str__(self):
        return "WordExp({})".format(self.name)

    def __repr__(self):
        return self.__str__()


class UnaryExpression(Expression):
    def __init__(self, operator, value1):
        self.operator = operator
        self.value1 = value1

    def evaluate(self):
        if self.operator is '+':
            return int(self.value1) 
        elif self.operator is '-':
            return -int(self.value1)
    
    def __str__(self):
        return "UnaryExp('{}', '{}')".format(
            self.operator, self.value1
        )

    def __repr__(self):
        return self.__str__()


class BinaryExpression(Expression):
    def __init__(self, operator, value1, value2):
        self.operator = operator
        self.value1 = value1
        self.value2 = value2

    def evaluate(self):
        if self.operator is '+':
            return int(self.value1) + int(self.value2) 
        elif self.operator is '-':
            return int(self.value1) - int(self.value2)
        elif self.operator is '*':
            return int(self.value1) * int(self.value2)
        elif self.operator is '/':
            if self.value2 == 0: raise ZeroDivisionError()
            return int(self.value1) / int(self.value2)
        else:
            raise TypeError("Unknown operator")
    
    def __str__(self):
        return "BinaryExp('{}', '{}', '{}')".format(
            self.value1, self.operator, self.value2
        )

    def __repr__(self):
        return self.__str__()