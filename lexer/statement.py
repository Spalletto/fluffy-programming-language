from variables import *
from expressions import *


class Statement():
    def execute(self):
        raise NotImplementedError()

class AssignStatement(Statement):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression
        self.result = 0
    
    def execute(self):
        self.result = int(self.expression)
        variables.add(self.variable, self.result)

    def __str__(self):
        return "AssignStatement({}: {})".format(
            self.variable, self.result
        )

    def print_vars(self):
        print(variables.VARIABLES)

class PrintStatement(Statement):
    def __init__(self, expression):
        self.expression = expression
        if type(expression) is int:
            self.expression = NumberExpression(expression)

    def execute(self):
        print(self.expression.evaluate())

    def __str__(self):
        return "PrintStatement(Text: '{}')".format(
            self.expression.evaluate()
        )
