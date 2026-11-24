import csv

"""
5.3 Handle CSV or JSON Files with Python Modules / Exporting and Importing Data

Serializing
How to exchange data

Serializing means to write your app data into an exchangeable format.

Deserializing means to convert data for your programs to use

There are several ways to exchange data, but two common formats that are used are CSV and JSON.

* Comma Separated Values(CSV)
    A Staple in TAbular Data

    Comma Separated Values are tabular data where each recor is stored in one rwo

    Data for each field is separated by commmas.

    While they can have consistency quirks, theey are popular with spreadsheet and pandas users.

    The csv module in Python can streamline exporting and importing CSV's.

* Javascript Objetc Notation (JSON)
    A Populat Interchange Format

    Javascript Object Notation (JSON) is a lighweight, readable format for data interchange.

    A lighter successot to XML, it is popular for web services and applications.

    The json module in Python can streamline the creation and export of JSON files,
    as well as importing them.

"""


class Contact:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email


contacts = [
    Contact("John", "Doe", "john.doe@example.com"),
    Contact("Jane", "Smith", "jane.smith@example.com"),
    Contact("Michael", "Johnson", "michael.johnson@example.com"),
    Contact("Emily", "Brown", "emily.brown@example.com"),
    Contact("David", "Wilson", "david.wilson@example.com"),
    Contact("Sarah", "Taylor", "sarah.taylor@example.com"),
    Contact("James", "Anderson", "james.anderson@example.com"),
    Contact("Laura", "Thomas", "laura.thomas@example.com"),
    Contact("Robert", "Jackson", "robert.jackson@example.com"),
    Contact("Jessica", "White", "jessica.white@example.com"),
    Contact("Daniel", "Harris", "daniel.harris@example.com"),
    Contact("Olivia", "Martin", "olivia.martin@example.com"),
    Contact("William", "Thompson", "william.thompson@example.com"),
    Contact("Sophia", "Garcia", "sophia.garcia@example.com"),
    Contact("Matthew", "Martinez", "matthew.martinez@example.com"),
    Contact("Emma", "Robinson", "emma.robinson@example.com"),
    Contact("Christopher", "Clark", "christopher.clark@example.com"),
    Contact("Isabella", "Rodriguez", "isabella.rodriguez@example.com"),
    Contact("Andrew", "Lewis", "andrew.lewis@example.com"),
    Contact("Mia", "Walker", "mia.walker@example.com"),
]

with open("contacts.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["first_name", "last_name", "email"])
    for c in contacts:
        writer.writerow([c.first_name, c.last_name, c.email])
