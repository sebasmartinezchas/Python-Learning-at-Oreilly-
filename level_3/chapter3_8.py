""""
Use Context Managers in Python / Managing Resources with "with"

Context Manager Protocol
1 . We start a block with the with keyboard, and an object.
2 . We can optionally assign that object to a variable using the as keyword.
3 . At the start of the block, the object's __enter__() method is executed.
4 . The block runs.
5 . At the end of the block, the object's __exit__() method is executed.

You can add this protocol to your classes!!
1 .If your class has both __enter__() and __exit__() methods, you can use it in a with statement.
2. At the start of the block, the __enter__() method is executed.
3. At the end of the block, the __exit__() method is executed.

"""
class LoudManager:
    def __init__(self,data):
        
        print(f"Now in LoudManager.__init__, with {data=}")
        self.data=data

    def __enter__(self):
        print(f"Now in LoudManager.__enter__, with {vars(self)}")
        return self

    def __exit__(self,exc_type,exc_value,traceback):
        print(f"Now in LoudManager.__exit__, with {vars(self)}")       
       # return True # This will suppress the exception and not propagate it  

lm=LoudManager(10)
print(f"Now in main, with {vars(lm)}")

with LoudManager(20) as lm:
    print("Hello from inside the with block")
    raise TypeError("This is a test exception") 
    print("You will not see this line because the exception will be raised before it is executed")