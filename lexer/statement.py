from variables import *


class Statement():
    def execute(self):
        raise NotImplementedError()

class AssignStatement(Statement):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression
        self.vars = Variables()
        self.result = 0
    
    def execute(self):
        self.result = int(self.expression)
        self.vars.add(self.variable, self.result)
        self.print_vars()

    def __str__(self):
        return "AssignStatement({}: {})".format(
            self.variable, self.result
        )
    def print_vars(self):
        print(self.vars.VARIABLES)