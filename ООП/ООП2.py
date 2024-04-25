from math import pi
from abc import abstractmethod

class Shape:
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def area(self):
        return f'Площа прямокутника = {self.a * self.b}'

class Circle(Shape):
    def __init__(self, r):
        self.r = r
    def area(self):
        return f'Площа круга = {pi * self.r**2}'

rectangle = Rectangle(10, 15)
circle = Circle(4)

print(rectangle.area())
print(circle.area())
