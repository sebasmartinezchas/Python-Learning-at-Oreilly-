class Calculator:
    """
    A simple calculator that performs basic arithmetic operations.

    >>> calc=Calculator()
    >>> calc.add(2,3)
    5
    >>> calc.multiply(4,5)
    20
    >>> len(calc.history)
    2

    """
    def __init__(self) -> None:
        self.history=[]

    def add(self,a,b):
        result=a+b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def multiply(self,a,b):
        result=a*b
        self.history.append(f"{a} * {b} = {result}")
        return result
