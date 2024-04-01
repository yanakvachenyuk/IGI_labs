def input_values():
    """Input integer values from user and validate them."""

    num_list = []
    while True:
        try:
            num = int(input("Введите целое число (0, чтобы закончить ввод) : "))
            if num == 0:
                break
            num_list.append(num)
        except ValueError:
            print("Ошибка. Необходимо целочисленное значение. Попробуйте еще раз")
    return num_list

def calculate_max(num_list):
    """Calculate the maximum number in the list."""

    max_num = max(num_list)
    return max_num

def calculate_sum(num_list):
    """Calculate the sum of the numbers in the list"""

    sum_num = sum(num_list)
    return sum_num

def task2_solve():
    """Solve task 2"""

    num_list = input_values()
    print(num_list)
    max_num = calculate_max(num_list)
    print(f"Максимальное число: {max_num}")
    sum_num = calculate_sum(num_list)
    print(f"Сумма чисел: {sum_num}")