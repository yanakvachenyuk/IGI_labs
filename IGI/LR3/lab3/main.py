from task1 import task1_solve
from task2 import task2_solve
from task3 import task3_solve
from task4 import task4_solve
from task5 import task5_solve

#Lab work 3 Standart tyoes, collections, modules, functions
#Kvachenyuk Yana 31.03.2024


if __name__ == '__main__':
    while True:
        while True:
            try:
                task_num = int(input("\nВведите номер задачи (0, чтобы завершить программу) : "))
                if task_num < 0 or task_num > 5:
                    raise ValueError("Номер задачи должен быть в диапазоне от 0 до 5")
                break
            except ValueError as e:
                if "invalid literal for int() with base 10" in str(e):
                    print("Ошибка: Введено не числовое значение. Попробуйте еще раз.")
                else:
                    print(f"Ошибка: {e}. Попробуйте еще раз.")
        if task_num == 1:
            task1_solve()
        elif task_num == 2:
            task2_solve()
        elif task_num == 3:
            task3_solve()
        elif task_num == 4:
            task4_solve()
        elif task_num == 5:
            task5_solve()
        elif task_num == 0:
            break


