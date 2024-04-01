# list_initialization.py

def input_list(lst, n):
    """Function to enter a list of n real numbers."""

    i = 0
    while i < n:
        num = input("Введите вещественное число: ")
        if validate_input(num):
            lst.append(float(num))
            i += 1
        else:
            print("Введено некорректное значение. Попробуйте еще раз.")
    return lst

def float_generator(n):
    """Generator function to generate n real numbers."""

    for i in range(n):
        yield float(i) + 1.25
def input_list_generator(lst, n):
    """Function to enter a list of n real numbers using a generator."""

    for num in float_generator(n):
        lst.append(num)

def validate_input(input_value):
    """Function to validate input value."""

    try:
        float(input_value)
        return True
    except ValueError:
        return False