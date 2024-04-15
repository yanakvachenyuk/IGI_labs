from Notebook import Notebook

def task1_solve():
    """Main function for task 1."""

    notebook = Notebook()
    csv_filename = 'notebook.csv'
    pickle_filename = 'notebook.pickle'
    while True:
        print('1 - Добавить новый элемент в список\n2 - Записать данные в csv файл\n3 - Загрузить данные из csv файла\n4 - Записать данные в pickle файл\n5 - Загрузить данные из pickle файла\n6 - Найти элемент по фамилии\n7 - Найти элемент по номеру телефона\n0 - Выйти из программы')
        try:
            choice = int(input('Ваш выбор: '))
            if choice < 0 or choice > 7:
                raise ValueError('Неверный выбор. Попробуйте еще раз.')
        except ValueError as e:
            print(f'Ошибка: {e}')

        if choice == 1:
            surname = input('Введите фамилию: ')
            while True:
                phone = input('Введите номер телефона (12-15 цифр): ')
                if not Notebook.validate_phone(phone):
                    print('Неверный формат номера телефона. Попробуйте еще раз.')
                    continue
                break
            notebook.add_entry(surname, phone)
        elif choice == 2:
            notebook.save_to_csv(csv_filename)
        elif choice == 3:
            notebook.load_from_csv(csv_filename)
            print('Загруженные данные:')
            for entry in notebook.entries:
                print(f'Surname: {entry["surname"]}, Phone: {entry["phone"]}')
        elif choice == 4:
            notebook.save_to_pickle(pickle_filename)
        elif choice == 5:
            notebook.load_from_pickle(pickle_filename)
            print('Загруженные данные:')
            for entry in notebook.entries:
                print(f'Surname: {entry["surname"]}, Phone: {entry["phone"]}')
        elif choice == 6:
            surname = input('Введите фамилию: ')
            print(notebook.find_by_surname(surname))
        elif choice == 7:
            phone = input('Введите номер телефона: ')
            print(notebook.find_by_phone(phone))
        elif choice == 0:
            break
