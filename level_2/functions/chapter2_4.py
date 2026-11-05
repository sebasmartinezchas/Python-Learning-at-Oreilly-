# Use Built in functions in Python Loops ( Looping Helpers)

favorite_fruits=["jujube","pear","watermelon","apple","blueberry"]
n=1
for fruit in favorite_fruits:
    print(n,fruit)
    n+=1

# Usando range !! No recomendado en bucles en python, tenemos enumerate.
print('------------------------------------------')
print('Usando range')
for i in range(len(favorite_fruits)):
    print(i+1,favorite_fruits[i])

# Usando enumerate -> devuelve una tupla
print("------------------------------------------")
print("Usando enumerate")
for item in enumerate(favorite_fruits):
    print(item)

# Podemos pasar un argunmento para decir donde empieza
print("------------------------------------------")
print("Usando start")
for item in enumerate(favorite_fruits,start=1):
    print(item)

# Question 3
for n in range(5):
    print(n)
