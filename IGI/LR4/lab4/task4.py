from abc import ABC, abstractmethod
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import math

class GeometricFigure(ABC):
    def __init__(self, input_name):
        """Initialize the object with the specified name."""

        self.name = input_name

    def get_name(self):
        """Return the name of the figure."""

        return self.name
    @abstractmethod
    def area(self):
        """Calculate the area of the figure."""

        pass

class Color:
    def __init__(self, color):
        """Initialize the object with the specified color."""

        self.hidden_color = color

    @property
    def color(self):
        """Return the color of the figure."""

        return self.hidden_color

    @color.setter
    def color(self, input_color):
        """Set the color of the figure."""

        self.hidden_color = input_color

class Triangle(GeometricFigure):
    def __init__(self, base, name, height, angle, color):
        """Initialize the object with the specified base, height, angle, and color."""

        super().__init__(name)
        self.base = base
        self.height = height
        self.angle = math.radians(angle)
        self.color = Color(color)

    def area(self):
        """Calculate the area of the triangle."""

        return 0.5 * self.base * self.height

    def get_info(self):
        """Return the information about the triangle."""

        return "Triangle {} of color {}, with base {}, height {}, angle {} has an area of {}".format(
            self.name, self.color.color, self.base, self.height, self.angle, self.area())

    def draw(self):

        fig, ax = plt.subplots(figsize=(8, 6))
        # calculate the coordinates of the vertices
        x2 = self.height * math.tan(self.angle)
        y2 = self.height
        vertices = [[0, 0], [self.base, 0], [x2, y2]]
        ax.add_patch(patches.Polygon(vertices, closed=True, color=self.color.color))
        plt.xlim(0, self.base + 1)
        plt.ylim(0, max(self.height, y2) + 1)
        plt.title(self.get_info(), fontsize=10)
        plt.tight_layout()
        plt.show()
        fig.savefig('triangle.png')


def validate_color():
    """Validate the color input from the user."""

    while True:
        color = input().lower()
        if color in colors.CSS4_COLORS:
            return color
        else:
            print("Неверный ввод. Пожалуйста, введите цвет из списка.")

def input_float_number():
    """Input a float number from the user."""

    while True:
        try:
            num = float(input())
            if num <= 0:
                raise ValueError("Число должно быть больше 0.")
            return num
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите десятичное число с плавающей точкой.")


def task4_solve():

    name = input("Enter the name of the triangle: ")
    print("Enter the base of the triangle: ")
    base = input_float_number()
    print("Enter the height of the triangle: ")
    height = input_float_number()
    print("Enter the angle of the triangle: ")
    angle = input_float_number()
    print("Enter the color of the triangle: ")
    color = validate_color()
    triangle = Triangle(base, name, height, angle, color)
    print(triangle.get_info())
    triangle.draw()