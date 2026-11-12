# Handle Mutabiility and Object references in Python
def create_shopping_lista(items=[]):
    items.append("milk")
    return items

monday_list=create_shopping_lista()
tuesday_list=create_shopping_lista()
wednesday_list=create_shopping_lista()

print("Monday's list:",monday_list)
print("Tuesday's list:",tuesday_list)
print("Wednesday's list:", wednesday_list)


# The correct way to create a shopping list is to use a default argument that is not mutable.
def create_shopping_list(items=None):
    if items is None:
        items = []
    items.append("milk")
    return items

monday_list=create_shopping_list()
tuesday_list=create_shopping_list()
wednesday_list=create_shopping_list()

print("Monday's list:",monday_list)
print("Tuesday's list:",tuesday_list)
print("Wednesday's list:", wednesday_list)

name=["Sam","Lau"]
foo=name
foo.append("Hello")

# Lists are mutable, so name and foo still point to the same list object
print("name:",name)
print("foo:",foo)

# Output:
# name: ['Sam', 'Lau', 'Hello']
# foo: ['Sam', 'Lau', 'Hello']

# Strings are immutable, so name and foo point to different objects
print("name:",name)
print("foo:",foo)


a=[1,2]
b=[1,2]

print(a==b)
print(a is b)

# Output:
# True
# False

# The == operator checks if the values are the same, while the is operator checks if the objects are the same.

c=a
print(a==c)
print(a is c)

# Assignment creates references, not copies.

d=a[:]
print(a==d)
print(a is d)

# Output:
# True
# False

# The [:] creates a new list object, so a and d are different objects.
# Copy method is not a deep copy, it is a shallow copy.

e=a.copy()
print(a==e)
print(a is e)

# Output:
# True
# False

# The copy method creates a new list object, so a and e are different objects.

class ShoppingCart:
    def __init__(self,items=None):
        if items is None:
            items = []
        self.items=items

    def add_item(self,item):
        self.items.append(item)

    def share_cart(self,other_cart) -> None:
        other_cart.items=self.items.copy() # This is a shallow copy of the items list. and it is ok for this case because the items list is not mutable.
        return other_cart

#Test the ShoppingCart class

cart1=ShoppingCart()
cart2=ShoppingCart()
cart1.add_item("laptop")
cart1.share_cart(cart2)
cart1.add_item("mouse")
print(f"cart1: {cart1.items}")
print(f"cart2: {cart2.items}")

# Output:
# cart1: ['laptop', 'mouse']
# cart2: ['laptop', 'mouse']
