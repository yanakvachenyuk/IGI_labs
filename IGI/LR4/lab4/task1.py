import csv
import pickle

class Notebook:
    def __init__(self):
        self.entries = []

    def add_entry(self, surname, phone):
        self.entries.append({'surname': surname, 'phone': phone})

    def save_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['surname', 'phone']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.entries)

    def load_from_csv(self, filename):
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            self.entries = list(reader)

    def save_to_pickle(self, filename):
        with open(filename, 'wb') as picklefile:
            pickle.dump(self.entries, picklefile)

    def load_from_pickle(self, filename):
        with open(filename, 'rb') as picklefile:
            self.entries = pickle.load(picklefile)

    def find_by_surname(self, surname):
        return [entry for entry in self.entries if entry['surname'].startswith(surname)]

    def find_by_phone(self, phone):
        return [entry for entry in self.entries if entry['phone'] == phone]