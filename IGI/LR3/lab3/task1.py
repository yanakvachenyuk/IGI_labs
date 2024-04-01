def calculate_function(x, eps):
    """Calculate the sum of the series 1 + x + x^2 + x^3 + ... with given accuracy eps."""

    term = 1
    sum = 1
    n = 0

    while abs(term) > eps and n < 500:
        term *= x
        sum += term
        n += 1

    return sum, n

def input_values():
    """Input x and eps values from user and validate them."""

    while True:
        try:
            x = float(input("Введите значение x такое, что (|x| < 1): "))
            if abs(x) >= 1:
                raise ValueError("Введенное значение должно быть меньше 1 по модулю")
            break
        except ValueError as e:
            if "could not convert string to float" in str(e):
                print("Ошибка: Введено не числовое значение. Попробуйте еще раз.")
            else:
                print(f"Ошибка: {e}. Попробуйте еще раз.")

    while True:
        try:
            eps = float(input("Введите точность вычислений eps: "))
            break
        except ValueError:
            print("Ошибка: Введено не числовое значение. Попробуйте еще раз.")
    return x, eps

def output_values(x, sum, n, eps):
    """Output x, n, sum, and math value of the function 1/(1-x) and eps to the console."""

    math_value = 1/(1-x)
    print(f"x : {x}")
    print(f"n : {n}")
    print(f"F(x) : {sum}")
    print(f"Math F(x) : {math_value}")
    print(f"eps : {eps}")

def task1_solve():
    """Solve task 1."""

    x, eps = input_values()
    sum, n = calculate_function(x, eps)
    output_values(x, sum, n, eps)