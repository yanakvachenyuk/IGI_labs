import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

class SequenceAnalyzer:
    def __init__(self, x, eps):
        """Initialize the object with the specified x and accuracy."""

        self.x = x
        self.eps = eps
        self.sequence, _ = self.calculate_function(x, eps)

    def mean(self):
        """Calculate the mean of the sequence."""

        return np.mean(self.sequence)

    def median(self):
        """Calculate the median of the sequence."""

        return np.median(self.sequence)

    def mode(self):
        """Calculate the mode of the sequence."""

        return float(stats.mode(self.sequence)[0])

    def variance(self):
        """Calculate the variance of the sequence."""

        return np.var(self.sequence)

    def standard_deviation(self):
        """Calculate the standard deviation of the sequence."""

        return np.std(self.sequence)

    def calculate_function(self, x, eps):
        """Calculate the sum of the series for the function (1 / (1 - x))."""

        term = 1
        series_sum = 1
        n = 0
        terms = []

        while abs(term) > eps and n < 500:
            term *= x
            series_sum += term
            n += 1
            terms.append(series_sum)

        return terms, n

    def plot_graphs(self, eps):
        """Plot the graph of the series and the function 1 / (1 - x)."""

        x_values = np.linspace(-0.99, 0.99, 100)

        y_values_series = []

        for xi in x_values:
            terms, n = self.calculate_function(xi, eps)
            y_values_series.append(terms[len(terms) - 1])

        y_values_math = [1 / (1 - xi) if xi != 1 else np.nan for xi in x_values]

        plt.plot(x_values, y_values_series, label='Разложение в ряд', color='blue')

        plt.plot(x_values, y_values_math, label='Функция (1/(1-x))', color='red', linestyle='--')

        max_y = max(y_values_series)
        max_x = x_values[y_values_series.index(max_y)]
        plt.annotate('Максимум ', xy=(max_x, max_y), xytext=(max_x - 0.5, max_y + 0.1), arrowprops=dict(facecolor='black', shrink=0.05))

        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Графики разложения функции в ряд и функции 1/(1-x)')

        plt.legend()

        plt.savefig('function_graph.png')

        plt.show()

