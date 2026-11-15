#Use Lambda Function in python/ Understanding anonymous functions
# What happens when we define a function
def square(x):
    return x * x

#print(square(5))

#print(square(15))
# What happens when we used def?
# 1. We create a function object value.
# 2. We assign the function object to a variable name.
# This is surprising to people come from other programming languages.
# Example
#square = 5
#print(square(10)) # This will raise an error because square is not a function. 'int' object is not callable

# What if we just wanto to create a function objectm and not assign it to a variable?
"""
'lambda' is a Python keyword that does the first thing( create a function object) but not the second thing
( assign the function object to a variable name).
lamba creates an anonymous function.

"""
words='this is a bunch of words'.split()
print(words)

sorted_words = sorted(words)
print(sorted_words) # By default, sorted will indeed sort them lexicographically and return a new list.

# I want to sort them by *length*
print(sorted(words,key=len))

# I want to sort backwards?

def by_backwards_word(text):
    return text[::-1]
print(sorted(words,key=by_backwards_word))

# We just define and entire function, and used up a name in our namespace,just sort these words once.
# It might be better to use a disposable, anonymous function.
"""
`lambda`
- First, we say `lambda`
- Then we can name one or more parameters, all without parenthesis,but with commas between them.
- Then we have a `:`
- Then we have a one-line Python expression-- no statements(for,while,return,assignments)
- The result of the expression is implicitly returned to the caller.

"""
print(sorted(words,key=lambda text: text[::-1]))
