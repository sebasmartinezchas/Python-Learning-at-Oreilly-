"""
Exercice Stats
1. Create a class that takes a list of numbers( ints or floats) as an argument.
2. The class should implement three methods:mean,min,max.
3. When we use this class in a with statement, then it should filter out any non-numbers in the input list.
4. When we exit from this class from a with block, then all three methods should be invoked, and their ouputs should be printed to the screen.


"""



class Stats:
    def __init__(self, numbers):
        self.numbers = numbers

    def __enter__(self):
        if not isinstance(self.numbers, list) :
            raise TypeError("Input must be a list of numbers.")
        self.numbers = [num for num in self.numbers 
                                           if isinstance(num, (int, float)) and not isinstance(num, bool) ]
        return self

    def mean(self):
        if len(self.numbers) == 0:
            raise ValueError("Cannot compute mean of an empty list.")
        return sum(self.numbers) / len(self.numbers)

    def min(self):
        return min(self.numbers)

    def max(self):
        return max(self.numbers)

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"Mean: {self.mean()}")
        print(f"Min: {self.min()}")
        print(f"Max: {self.max()}")



with Stats([1, 2, 3, 4, 5, 'a', None,True,False, 6.5]) as stats:
    print("Inside the with block")
    # You can access the filtered numbers if needed
    print(f"Filtered numbers: {stats.numbers}")