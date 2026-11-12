"""
Guided Practice Example: Debugging with Print Statements and pdb

"""

def uses_none(word,forbidden):
    """Checks wheter a word avoids forbidden letters.
    >>> uses_none('banana','xyz')
    True
    >>> uses_none('apple','efg')
    False
    """
    for letter1 in word:
        for letter2 in forbidden:
            breakpoint()
            if letter1==letter2:
                return False

    return True





#print(uses_none('banana','xyz'))

print(uses_none("apple", "efg"))
