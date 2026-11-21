x='global'

def outer():
    x='enclosing' # Enclosing scope
    #print(x)
    def inner():
        x='local' # Local scope
        print(x) # Local
    inner()
    print(x) # Enclosing 
    #de la función ourter para que no lo imprima dos veces).

outer()   
print(x)    # 'goblal'

# Built-in example
print(len('built-in')) # 'len' is buit-in