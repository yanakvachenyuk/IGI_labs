import task1_solve
import task2_solve
import task3_solve
import task4
import task5
import math

# Lab work 4 Classes, files, serialization, regular expressions and standard libraries
# Kvachenyuk Yana 14.04.2024

if __name__ == '__main__':
    while True:
        while True:
            try:
                task_num = int(input("\nВведите номер задачи (0, чтобы завершить программу) : "))
                if task_num < 0 or task_num > 5:
                    raise ValueError("Номер задачи должен быть в диапазоне от 0 до 5")
                break
            except ValueError as e :
                    print(f"Ошибка: {e}. Попробуйте еще раз.")
        if task_num == 1:
            task1_solve.task1_solve()
        elif task_num == 2:
            task2_solve.task2_solve()
        elif task_num == 3:
            task3_solve.task3_solve()
        elif task_num == 4:
            task4.task4_solve()
        elif task_num == 5:
            task5.task5_solve()
        elif task_num == 0:
            break

