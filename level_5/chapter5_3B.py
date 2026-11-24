import csv


class Contact:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email


contacts = []

with open("contacts.csv", "r", encoding="utf-8", newline="") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        contacts.append(Contact(row["first_name"], row["last_name"], row["email"]))
        for contact in contacts:
            print(contact.first_name, contact.last_name, contact.email)

