import json

class Contact:
    def __init__(self,first_name,last_name,email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

contacts = []

with open("contacts.json", "r", encoding='utf-8') as f:
    contacts_data = json.load(f)
    for contact in contacts_data:
        contacts.append(Contact(
            contact["first_name"],
            contact["last_name"],
            contact["email"]
        ))
for c in contacts:
    print(f"{c.first_name} {c.last_name} - {c.email}")