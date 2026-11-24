import json

class Contact:
    def __init__(self,first_name,last_name,email):
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

with open("contacts.json", "w", encoding='utf-8') as f:
    json.dump([{
        "first_name": contact.first_name,
        "last_name": contact.last_name,
        "email": contact.email
    } for contact in contacts], f,indent=4)
