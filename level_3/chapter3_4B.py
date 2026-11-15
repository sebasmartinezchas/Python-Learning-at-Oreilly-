"""
Exercise:Product with a read-only ID number.
Imagine you're designing a system for an warehouse. Every new product you create
needs it's own ID number(SKU).It should be possible to get the ID number via an
attribute, but trying to set it should raise an exception. You can only set the ID number
once when you create the product.
"""
class Product:
    def __init__(self,name,sku):
        self.name=name
        self._sku=sku

    @property
    def sku(self):
        return self._sku
