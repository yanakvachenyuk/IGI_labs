import re
import zipfile
from collections import Counter

class TextAnalyzer:
    def __init__(self, input_file, output_file, archive_file):
        """Initialize the text analyzer."""

        self.input_file = input_file
        self.output_file = output_file
        self.archive_file = archive_file
        self.text = ""
        self.sentences = []
        self.all_words = []
        self.sentence_types = {'declarative': 0, 'interrogative': 0, 'imperative': 0}
        self.smileys = []
        self.valid_emails = []
        self.count_words_in_line = {}

    def load_text(self):
        """Load the text from the input file."""

        with open(self.input_file, 'r') as file:
            self.text = file.read()

    def analyze_text(self):
        """Analyze the text."""

        self.sentences = re.split(r'(?<=[.!?])[ +\n]', self.text)
        self.all_words = self.find_words(self.text)
        self.sentence_types = self.count_sentence_types(self.sentences)
        self.smileys = self.find_smileys(self.text)


        lines = self.text.splitlines()

        for line in lines:
            line = line.strip()
            if self.is_valid_email(line):
                self.valid_emails.append(line)

        for ind, line in enumerate(lines):
            word_count = len(self.find_words(line))
            self.count_words_in_line[ind] = word_count


    def find_words(self, text):
        """Find all words in the text."""

        words = re.findall(r'\b\w+\b', text)
        return words

    def find_words_in_range(self):
        """Find words containing characters from 'g' to 'o'."""
        words_in_range = [word for word in self.all_words if re.search(r'[g-o]', word)]
        return words_in_range

    def is_valid_email(self, email):
        """Check if the email is valid."""

        pattern = r'^\w+@\w+\.[a-zA-Z]{2,}$'
        #pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def count_sentence_types(self, sentences):
        """Count the number of each sentence type."""

        for sentence in sentences:
            if sentence.endswith('.'):
                self.sentence_types['declarative'] += 1
            elif sentence.endswith('?'):
                self.sentence_types['interrogative'] += 1
            elif sentence.endswith('!'):
                self.sentence_types['imperative'] += 1
        return self.sentence_types

    def find_smileys(self, text):
        """Find all smileys in the text."""

        pattern = r'[;:]-*[\(\[\)\]]+'
        smileys_found = re.findall(pattern, text)
        return smileys_found

    def find_longest_word(self):
        """Find the longest word in the text."""

        longest_word = ""
        longest_word_index = -1
        for ind, word in enumerate(self.all_words):
            if len(word) > len(longest_word):
                longest_word = word
                longest_word_index = ind
        return longest_word, longest_word_index

    def odd_words(self):
        """Find all words with odd indexes."""

        odd_words = [word for idx, word in enumerate(self.all_words) if idx % 2 != 0]
        return odd_words

    def save_results(self):
        """Save the results to the output file."""

        sentence_count = len(self.sentences)
        word_count = len(self.all_words)
        smiley_count = len(self.smileys)
        words_in_range = self.find_words_in_range()
        longest_word, longest_word_index = self.find_longest_word()

        odd_words = self.odd_words()

        total_word_length = sum(len(word) for word in self.all_words)
        avg_sentence_length = total_word_length / sentence_count

        avg_word_length = total_word_length / word_count

        with open(self.output_file, 'w') as file:
            file.write(f"Number of sentences: {sentence_count}\n")
            file.write(f"Number of declarative sentences: {self.sentence_types['declarative']}\n")
            file.write(f"Number of interrogative sentences: {self.sentence_types['interrogative']}\n")
            file.write(f"Number of imperative sentences: {self.sentence_types['imperative']}\n")
            file.write(f"Average sentence length: {avg_sentence_length}\n")
            file.write(f"Average word length: {avg_word_length}\n")
            file.write(f"Number of smileys: {smiley_count}\n")
            file.write("Words containing characters from 'g' to 'o':\n")
            file.write(", ".join(words_in_range) + "\n")
            file.write("Valid emails:\n")
            file.write("\n".join(self.valid_emails) + "\n")
            file.write("Word count per line:\n")
            for line_num, word_count in self.count_words_in_line.items():
                file.write(f"Line {line_num}: {word_count}\n")
            file.write(f"Longest word: {longest_word} (Index: {longest_word_index})\n")
            file.write("Odd indexed words:\n")
            file.write(", ".join(odd_words) + "\n")


        print(f"Number of sentences: {sentence_count}")
        print(f"Number of declarative sentences: {self.sentence_types['declarative']}")
        print(f"Number of interrogative sentences: {self.sentence_types['interrogative']}")
        print(f"Number of imperative sentences: {self.sentence_types['imperative']}")
        print(f"Average sentence length: {avg_sentence_length}")
        print(f"Average word length: {avg_word_length}")
        print(f"Number of smileys: {smiley_count}")
        print("Words containing characters from 'g' to 'o':")
        print(", ".join(words_in_range))
        print("Valid emails:")
        print("\n".join(self.valid_emails))
        print("Word count per line:")
        for line_num, word_count in self.count_words_in_line.items():
            print(f"Line {line_num}: {word_count}")
        print(f"Longest word: {longest_word} (Index: {longest_word_index})\n")
        print("Odd indexed words:")
        print(", ".join(odd_words))

    def archive_results(self):
        """Archive the output file."""

        with zipfile.ZipFile(self.archive_file, 'w') as zipf:
            zipf.write(self.output_file)
