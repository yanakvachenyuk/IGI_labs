def count_all_chars_decorator(func):
    """Decorator that counts the total number of characters in the text."""

    def wrapper(text):
        total_chars = sum(char.isalpha() for char in text)
        print(f"Общее число букв: {total_chars}")
        return func(text)
    return wrapper

@count_all_chars_decorator
def count_chars(text):
    """Returns the number of characters 'g' to 'o' in the text."""

    count = 0
    for char in text:
        if 'g' <= char <= 'o':
            count += 1
    return count

def task3_solve():
    """Solve task 3"""

    text = input("Введите текст: ")
    count = count_chars(text)
    print(f"Количество символов от 'g' до 'o': {count}")