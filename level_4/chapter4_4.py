# Use super () to call Parent Methods in Python / How Does a Child on its Parent


class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def get_description(self):
        return f"{self.name}: ${self.price} "


class Pastry(MenuItem):
    def __init__(self, name, price, is_gluten_free=False):
        super().__init__(name, price)
        self.is_gluten_free = is_gluten_free

    def get_description(self):
        base_description = super().get_description()
        return f"{base_description} {' (GF) ' if self.is_gluten_free else ''}"


pastry = Pastry("Croissant", 2.00)
print(pastry.get_description())

gf_pastry = Pastry("Vanilla Bean Donut", 4.50, is_gluten_free=True)
print(gf_pastry.get_description())
