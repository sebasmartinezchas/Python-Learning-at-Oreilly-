# Define Instance Methods in Python/ Adding Methods to a class
from curses import KEY_SAVE
from level_2.functions.chapter2_10 import contact


class Contact:
    def __init__(self,first_name,last_name,email):
        self.first_name=first_name
        self.last_name=last_name
        self.email=email

    def send_email(self,message,priority="Normal"):
        print(f"Sending email to {self.email} with priority {priority}")
        print("Done!")  
        
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"Name: {self.full_name}Email: <{self.email}>"

contact=Contact("Alice","Smith","alice.smith@example.com")
contact.send_email("Hello, how are you?",priority="High")
#print(contact.full_name)

# Exercise:Book
# Create a class called Book.
# The Book class should have three attributes: title, author, and price.
# Add a taxed price method
# Accept a tax_rate argument with a default value of 0.07
# The tax_rate is added to 1.0, and that sum is multiplied against the price.
# The value above is returned
class Book:
    def __init__(self,title,author,price):
        self.title=title
        self.author=author
        self.price=price

    def taxed_price(self,tax_rate=0.07):
        return f"{self.price * (1 + tax_rate):.2f}"

book=Book("The Very Hungry Caterpillar","Eric Carle",5.00)
taxed_price=book.taxed_price()
# outputs: 5.35
taxed_price=book.taxed_price(0.05)
print(taxed_price)
# outputs: 5.25