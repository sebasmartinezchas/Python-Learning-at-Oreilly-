# Access and Modify Python Objet Attributes / Introducing Encapsulation
class Dog:
    def __init__(self,name,age,breed) -> None:
        self.name=name
        self.age=age
        self.breed=breed

    def set_age(self,new_age):
        if new_age >=0:
            self.age=new_age
        else:
            raise ValueError("Age cannot be negative.")

    def increment_age(self):
        self.age+=1

my_dog=Dog("Buddy",3,"Golden Retriever")


# It's Buddy's birthday! | Access directly
my_dog.increment_age()
print(f"Buddy is now {my_dog.age} years old.")

