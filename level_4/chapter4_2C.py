"""
There is a bug in this program due to the `print()`
being in the wrong place. Try to fix it so every number
is printed in the countdown from 10 through 0.

"""
n=10

def countdown(n):
    n+=1
    while n > 0:
        n-=1
        print(n)

#print(n) Scope global

countdown(n)
