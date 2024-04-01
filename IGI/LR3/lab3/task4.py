def word_count(text):
    """Returns the number of words in the text."""

    words = text.split()
    return len(words)

def letter_repetition(text):
    """Returns the number of repetitions of each letter in the text."""

    letter_counts = {}
    for letter in text.lower():
        if letter.isalpha():
            if letter in letter_counts:
                letter_counts[letter] += 1
            else:
                letter_counts[letter] = 1
    return letter_counts

def alphabetical_phrases(text):
    """Returns the phrases separated by commas in alphabetical order."""

    phrases = [phrase.strip() for phrase in text.lower().split(',')]
    phrases.sort()
    return phrases

def task4_solve():
    """Solve task 4"""

    text = "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."
    print(f"Анализируемый текст:\n{text}")

    count = word_count(text)
    print(f"\nа) число слов, ограниченных пробелами: {count}")

    print("\nб) количество повторений каждой буквы:")
    letter_counts = letter_repetition(text)
    print(sorted(letter_counts.items()))


    phrases = alphabetical_phrases(text)
    print("\nв) словосочетания, отделенные запятыми, в алфавитном порядке:\n")
    for phrase in phrases:
        print(phrase)



