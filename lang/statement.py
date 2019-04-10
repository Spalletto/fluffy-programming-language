from ast import literal_eval
from re import findall

from descartes import PolygonPatch
from shapely.geometry import Point, Polygon
from expressions import *
from lexer import PATCHES
from variables import *

import matplotlib.pyplot as plt

class Statement:
    def execute(self):
        raise NotImplementedError()


class AssignStatement(Statement):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression
        self.result = 0
    
    def execute(self):
        self.result = self.expression.evaluate()
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

    def execute(self):
        print(self.expression.evaluate())

    def __str__(self):
        return "PrintStatement(Text: '{}')".format(
            self.expression.evaluate()
        )


class DrawStatement(Statement):
    def __init__(self, variable, color):
        self.variable = variable
        self.color = color

    def execute(self):
        variable = self.variable.evaluate()
        str_variable = str(self.variable).replace("WordExp(", '').replace(')', '')

        if type(variable) is not str:
            raise TypeError(f"Wrong type for draw function. Figure expected, got '{type(variable)}'")

        if variable.startswith('Circle'):
            values = findall('[0-9]+', variable)
            values = list(map(int, values))
            x, y, r = values
            figure = Point(x, y).buffer(r)
        elif variable.startswith('Polygon'):
            variable = variable.replace('Polygon', '')
            points = literal_eval(variable)
            figure = Polygon(points)
        elif variable.startswith('DrawObject'):
            objects = variable.replace('DrawObject(', '').replace(')', '')
            function, obj1, obj2 = objects.split(',')
            obj1 = variables.get_object(obj1.strip())
            obj2 = variables.get_object(obj2.strip())
            
            if function == 'intersection':
                figure = obj1.intersection(obj2)
            if function == 'union':
                figure = obj1.union(obj2)
            if function == 'difference':
                figure = obj1.difference(obj2)
            if function == 'symmetric_difference':
                figure = obj1.symmetric_difference(obj2)
        else:
            raise TypeError(f"Wrong type for draw function. Figure expected, got '{type(variable)}'")
        
        variables.add_object(str_variable, figure)
        patch = PolygonPatch(figure, fc=self.color)
        PATCHES.append(patch)

    def __str__(self):
        return "DrawStatement(Text: '{}')".format(
            self.variable.evaluate()
        )


class ClearStatement(Statement):
    def execute(self):
        plt.cla()
        PATCHES.clear()
        plt.xlim(-2.5, 2.5)
        plt.ylim(-2.5, 2.5)

    def __str__(self):
        return "ClearStatement()"


class IfStatement(Statement):
    def __init__(self, expression, if_statement, else_statement):
        self.expression = expression
        self.if_statement = if_statement
        self.else_statement = else_statement

    def execute(self):
        result = self.expression.evaluate()
        if result != 0:
            self.if_statement.execute()
        elif self.else_statement is not None:
            self.else_statement.execute()

    def __str__(self):
        result = "If('{}') {}".format(
            self.expression, self.if_statement
        )
        if self.else_statement is not None:
            result += "\nElse {}".format(self.else_statement)
        return result


class BlockStatement(Statement):
    def __init__(self):
        self.statements = []

    def add(self, statement):
        self.statements.append(statement)
    
    def execute(self):
        for statement in self.statements:
            statement.execute()

    def __str__(self):
        return "BlockStatement('{}')".format(
            self.statements
        )


class WhileStatement(Statement):
    def __init__(self, condition, statement):
        self.condition = condition
        self.statement = statement

    def execute(self):
        while self.condition.evaluate() != 0:
            self.statement.execute()

    def __str__(self):
        return "WhileStatement('{}' : {})".format(
            self.condition, self.statement
        )


class ForStatement(Statement):
    def __init__(self, initialization, termination, increment, statement):
        self.initialization = initialization
        self.termination = termination
        self.increment = increment
        self.statement = statement

    def execute(self):
        self.initialization.execute()
        while self.termination.evaluate() != 0:
            self.statement.execute()
            self.increment.execute()

    def __str__(self):
        return "ForStatement({}, {}, {} : {})".format(
            self.initialization, self.termination, self.increment, self.statement
        )