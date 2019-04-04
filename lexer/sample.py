from shapely import *
from shapely.geometry import *

a = Point(1, 1).buffer(1.5)
b = Point(2, 1).buffer(1.5)

a.union(b)

