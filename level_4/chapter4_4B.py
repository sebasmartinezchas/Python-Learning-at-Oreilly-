"""
Extends the MenuItem class to CoffeDrink class with the following attributes added:
* coffe_type(str)
* size(int)


The append the get_description () method of the parent with those two attributes also added
to the returned string.


"""


class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def get_description(self):
        return f"{self.name} Price: ${self.price} "


class Pastry(MenuItem):
    def __init__(self, name, price, is_gluten_free=False):
        super().__init__(name, price)
        self.is_gluten_free = is_gluten_free

    def get_description(self):
        base_description = super().get_description()
        return f"{base_description} {' (GF) ' if self.is_gluten_free else ''}"


class CoffeDrink(MenuItem):
    def __init__(self, name, price, coffe_type, size):
        super().__init__(name, price)
        self.coffe_type = coffe_type
        self.size = size

    def get_description(self):
        base_description = super().get_description()
        return f"{base_description} {self.coffe_type}, {self.size} ounces"



cappuchino = CoffeDrink("Latte", 5.00, "Espresso",20)
print(cappuchino.get_description())
