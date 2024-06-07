import csv
import pickle
import re

class Notebook:

    def __init__(self):
        """Initialize the notebook."""

        self.entries = []

    def add_entry(self, surname, phone):
        """Add a new entry to the notebook."""

        self.entries.append({'surname': surname, 'phone': phone})

    @staticmethod
    def validate_phone(phone):
        """Check if the phone number is valid."""

        phone_regex = re.compile(r'^\+\d{12,15}$')
        return bool(phone_regex.match(phone))

    def save_to_csv(self, filename):
        """Save the notebook entries to a csv file."""

        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['surname', 'phone']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.entries)

    def load_from_csv(self, filename):
        """Load the notebook entries from a csv file."""

        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            self.entries = list(reader)

    def save_to_pickle(self, filename):
        """Save the notebook entries to a pickle file."""

        with open(filename, 'wb') as picklefile:
            pickle.dump(self.entries, picklefile)

    def load_from_pickle(self, filename):
        """Load the notebook entries from a pickle file."""

        with open(filename, 'rb') as picklefile:
            self.entries = pickle.load(picklefile)

    def find_by_surname(self, surname):
        """Find the entries with the given surname."""

        return [entry for entry in self.entries if entry['surname'].startswith(surname)]

    def find_by_phone(self, phone):
        """Find the entries with the given phone number."""

        return [entry for entry in self.entries if entry['phone'] == phone]