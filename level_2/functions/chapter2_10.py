# Store and Retrieve data with Python Objects
class Contact:
    def __init__(self,id,first_name,last_name,email):
        self.id=id
        self.first_name=first_name
        self.last_name=last_name
        self.email=email

contacts=[

    Contact(1,"Alice","Smith","alice@example.com"),
    Contact(2,"Bobby","Raymond","bobby@example.com"),
]

for contact in contacts:
    print(f"Contact: {contact.id} {contact.first_name} {contact.last_name},Email:{contact.email}")

class CoffeMenuItem():
    def __init__(self,name,price,size):
        self.name=name
        self.price=price
        self.size=size

items=[
    CoffeMenuItem("Latte",5.50,20),
    CoffeMenuItem("Cold Brew",4.50,16),
]

for item in items:
    print(f"Drink Name: {item.name} | Price: ${item.price} | Size: {item.size} ounces per serving")
