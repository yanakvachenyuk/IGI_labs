import numpy as np


class MyStd:
    def __init__(self, n, m):
        self.matrix = np.random.randint(0, 100, size=(n, m))

    def my_std(self):
        """Calculate the standard deviation of the matrix elements."""

        mean_value = np.mean(self.matrix)
        squared_diff = np.mean((self.matrix - mean_value) ** 2)   #среднее квадратичное отклонение.
        std_deviation_manual = np.sqrt(squared_diff)

        std_deviation_manual = round(std_deviation_manual, 2)
        return std_deviation_manual

class MatrixMixin:
    def make_matrix(self, n, m):
        """Create a matrix with random values."""

        return np.random.randint(0, 100, size=(n, m))

class WorkWithMatrix(MyStd, MatrixMixin):
    instance_count = 0
    def __init__(self, n, m):
        """Initialize the object with the specified number of rows and columns."""

        self.matrix = self.make_matrix(n, m)
        WorkWithMatrix.instance_count += 1

    def __str__(self):
        """Return the matrix as a string."""

        return '\n'.join([' '.join(map(str, row)) for row in self.matrix])

    def count_min_elements(self):
        """Count the number of minimum elements in the matrix."""

        min_value = np.min(self.matrix)
        min_count = np.count_nonzero(self.matrix == min_value)
        min_indices = np.where(self.matrix == min_value)
        return min_value, min_count, min_indices

    def numpy_std(self):
        """Calculate the standard deviation of the matrix elements."""

        std_deviation = np.std(self.matrix)
        return round(std_deviation, 2)




def task5_solve():
    """Create a matrix and display the minimum element, the number of minimum elements, and the standard deviation."""

    print("Введите количество строк матрицы: ")
    n = input_natural_number()
    print("Введите количество столбцов матрицы: ")
    m = input_natural_number()
    matrix_work = WorkWithMatrix(n, m)
    print("Матрица:")
    print(matrix_work)
    min_value, min_count = matrix_work.count_min_elements()
    print(f"Минимальный элемент: {min_value}, количество: {min_count}")
    print(f"Стандартное отклонение (numpy):{matrix_work.numpy_std()}")
    print(f"Стандартное отклонение (manual):{matrix_work.my_std()}")
    print(f"Количество созданных объектов: {WorkWithMatrix.instance_count}")

def input_natural_number():
    """Input a natural number from the user."""

    while True:
        try:
            num = int(input())
            if num < 1:
                print("Неверный ввод. Пожалуйста, введите натуральное число.")
                continue
            return num
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите натуральное число.")
