import numpy as np

class MatrixMixin:
    def make_matrix(self, n, m):
        """Create a matrix with random values."""

        return np.random.randint(0, 100, size=(n, m))

class WorkWithMatrix(MatrixMixin):
    instance_count = 0
    def __init__(self, n, m):
        self.matrix = self.make_matrix(n, m)
        WorkWithMatrix.instance_count += 1

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.matrix])

    def count_min_elements(self):
        min_value = np.min(self.matrix)
        min_count = np.count_nonzero(self.matrix == min_value)
        return min_value, min_count

    def numpy_std(self):
        """Calculate the standard deviation of the matrix elements."""
        std_deviation = np.std(self.matrix)
        return round(std_deviation, 2)

    def my_std(self):
        mean_value = np.mean(self.matrix)
        squared_diff = np.mean((self.matrix - mean_value) ** 2)   #Sum of squares of deviations.
        std_deviation_manual = np.sqrt(squared_diff)

        std_deviation_manual = round(std_deviation_manual, 2)
        return std_deviation_manual


def task5_solve():

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
