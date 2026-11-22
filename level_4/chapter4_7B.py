# Making a iterator in Python
class CountDown:
    """Iterator which counts downward from a given number to 0"""
    def __init__(self,start):
        self.n=start

    def __next__(self):
        if self.n<=0:
            raise StopIteration("o reached")
        number=self.n
        self.n-=1
        return number

    def __iter__(self):
        return self

counter=CountDown(3)
print(next(counter)) # output 3 
print(list(counter)) # output [2,1]


# Es muy raro hacer esto, lo más común es usar un generador => generator expression or generator function
# Notese que estamos exponiendo un atributo .n que podemos modificar
counter.n=5
print(next(counter)) # output 5
print(list(counter)) # [4,3,2,1]

