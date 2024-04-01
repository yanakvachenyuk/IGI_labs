import list_initialization

def process_list(lst):
    """Return the minimum positive number and the sum of the numbers between the first and last."""

    positive_nums = [num for num in lst if num > 0]
    if not positive_nums:
        return None, None
    min_positive = min(positive_nums)
    first_positive_index = next(i for i, num in enumerate(lst) if num > 0)
    last_positive_index = len(lst) - 1 - next(i for i, num in enumerate(lst[::-1]) if num > 0)
    sum_between = sum(lst[first_positive_index + 1:last_positive_index])
    return min_positive, sum_between


def print_list(lst):
    """Print the list."""

    print("Список:", lst)

def input_list(lst):
    """Input a list of n real numbers."""

    print("\nВыберите способ создания списка\n1 - С помощью пользовательского ввода\n2 - С помощью функции генератора\n")
    while True:
        try:
            sub_task_num = int(input("Введите значение для выбора: "))
            if sub_task_num != 1 and sub_task_num != 2:
                raise ValueError("Введено некорректное значение. Введите 1 или 2.")
            break
        except ValueError as e:
            if "invalid literal for int() with base 10" in str(e):
                print("Ошибка: Введено не числовое значение. Попробуйте еще раз.")
            else:
                print(f"Ошибка: {e}. Попробуйте еще раз.")

    while True:
        try:
            n = int(input("Введите размерность списка: "))
            if n <= 0:
                raise ValueError("Размерность списка должна быть положительным числом.")
            break
        except ValueError as e:
            if "invalid literal for int() with base 10" in str(e):
                print("Ошибка: Введено не числовое значение. Попробуйте еще раз.")
            else:
                print(f"Ошибка: {e}. Попробуйте еще раз.")

    if sub_task_num == 1:
        list_initialization.input_list(lst, n)
    elif sub_task_num == 2:
        list_initialization.input_list_generator(lst, n)


def task5_solve():
    """Solve task 5."""

    lst = []
    input_list(lst)

    while True:
        print("\n1 - Ввести новый список\n2 - Вывести список\n3 - Найти минимальный положительный элемент списка и "
              "сумму элементов списка, расположенных между первым и последним положительными элементами\n0 - "
              "завершить задание\n")
        while True:
            try:
                task_num = int(input("Введите номер функции : "))
                if task_num < 0 or task_num > 3:
                    raise ValueError("Введенное значение должно быть в диапазоне от 0 до 3.")
                break
            except ValueError as e:
                if "invalid literal for int() with base 10" in str(e):
                    print("Ошибка: Введено не числовое значение. Попробуйте еще раз.")
                else:
                    print(f"Ошибка: {e}. Попробуйте еще раз.")
        if task_num == 1:
            lst.clear()
            input_list(lst)

        elif task_num == 2:
            print_list(lst)
        elif task_num == 3:
            min_positive, sum_between = process_list(lst)
            if min_positive is None:
                print("В списке нет положительных чисел.")
            else:
                print(f"Минимальное положительное число: {min_positive}")
                print(f"Сумма чисел между первым и последним положительными числами: {sum_between}")
        elif task_num == 0:
            break
