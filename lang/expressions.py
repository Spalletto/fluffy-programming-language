from variables import variables
from shapely.geometry import Point, Polygon
from ast import literal_eval


class Expression:
    def evaluate(self):
        raise NotImplementedError


class ValueExpression(Expression):
    def __init__(self, value):
        self.value = value
    
    def __int__(self):
        return self.value
    
    def evaluate(self):
        return self.value

    def __str__(self):
        return "ValueExpession({})".format(self.value)

    def __repr__(self):
        return self.__str__()


class ConstantExpression(Expression):
    def __init__(self, name):
        self.name = name

    def evaluate(self):
        result = variables.VARIABLES.get(self.name)
        if result is None: 
            raise NameError("Variable '{}' doesn't exist".format(self.name))
        else: 
            return result['value']

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
            return self.value1
        elif self.operator is '-':
            return -self.value1.evaluate()
    
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
            return self.value1.evaluate() + self.value2.evaluate() 
        elif self.operator is '-':
            return self.value1.evaluate() - self.value2.evaluate() 
        elif self.operator is '*':
            return self.value1.evaluate() * self.value2.evaluate() 
        elif self.operator is '/':
            if self.value2 == 0: raise ZeroDivisionError()
            return self.value1.evaluate() // self.value2.evaluate() 
        else:
            raise TypeError("Unknown operator")
    
    def __str__(self):
        return "BinaryExp('{}', '{}', '{}')".format(
            self.value1, self.operator, self.value2
        )

    def __repr__(self):
        return self.__str__()


class ConditionalExpression(Expression):
    def __init__(self, operator, expr1, expr2):
        self.operator = operator
        self.expr1 = expr1
        self.expr2 = expr2

    def evaluate(self):  
        if self.operator is '=':
            return int(self.expr1.evaluate() == self.expr2.evaluate())
        elif self.operator is '<':
            return int(self.expr1.evaluate() < self.expr2.evaluate())
        elif self.operator is '>':
            return int(self.expr1.evaluate() > self.expr2.evaluate())
        else:
            raise TypeError("Unknown operator")

    def __str__(self):
        return "ConditionalExp('{}', '{}', '{}')".format(
            self.expr1, self.operator, self.expr2
        )

    def __repr__(self):
        return self.__str__()


class CircleObject(Expression):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def evaluate(self):
        return Point(self.center.x.evaluate(), self.center.y.evaluate()).buffer(self.radius.evaluate())

    def __str__(self):
        return "Circle(({}, {}), r={})".format(self.center.x.evaluate(), self.center.y.evaluate(), self.radius.evaluate())


class PolygonObject(Expression):
    def __init__(self, points):
        self.points = points
        self.evaluated_points = []

    def evaluate(self):
        for point in self.points:
            self.evaluated_points.append(point.evaluate())
       
        return Polygon(self.evaluated_points)

    def __str__(self):
        return "Polygon(" + ', '.join(self.evaluated_points) + ')'


class PointObject(Expression):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def evaluate(self):
        return (self.x.evaluate(), self.y.evaluate())

    def __str__(self):
        return "Point({}; {})".format(self.x, self.y)


class DrawObject(Expression):
    def __init__(self, function, obj1, obj2):
        self.function = function
        self.obj1 = obj1
        self.obj2 = obj2

    def evaluate(self):
        variable1 = variables.get(self.obj1)['value']
        variable2 = variables.get(self.obj2)['value']
        if self.function == 'intersection':
            figure = variable1.intersection(variable2)
        elif self.function == 'union':
            figure = variable1.union(variable2)
        elif self.function == 'difference':
            figure = variable1.difference(variable2)
        elif self.function == 'symmetric_difference':
            figure = variable1.symmetric_difference(variable2)
        else:
            raise NameError("There is no such a function: {}".format(self.function))
        
        return figure

    def __str__(self):
        return "DrawObject({}, {}, {})".format(self.function, self.obj1, self.obj2)