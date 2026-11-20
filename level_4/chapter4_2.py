x='global'

def outer():
    x='enclosing'
    print(x)

outer() # output => 'enclosing' 