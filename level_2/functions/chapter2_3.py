# List Comprehension in Python | Making New List from Old List
videos=[
    "Modules",
    "Sequences",
    "Slicing",
    "Tuple unpacking",
    "Truthiness",
    "Duck typing",
]
slugs=[]

for name in videos:
    slugs.append(name.lower().replace(" ", "-"))

for slug in slugs:
    print(slug)


# En lugar de escribir ese loop podríamos haber escrito una lista de comprensión
slugs=[name.lower().replace(" ","-")for name in videos]

# Otro ejemplo
single_word_names=[]
for name in videos:
    if " " not in name:
        single_word_names.append(name)

print(single_word_names)

# Es lo mismo que hacer
single_word_names=[name for name in videos if " " not in name]

print("Versión Comprehensión List")
print(single_word_names)


# Question 1
numbers=[10,11,12,13,14,15]
new_numbers=[n for n in numbers if n%2!=0]
print(new_numbers)

# Question 2
new_numbers_1=[n for n in numbers * 2 if n > 1]
print(new_numbers_1)
new_numbers_2=[n *2 for n in numbers if n > 1]
print(new_numbers_2)
new_numbers_3=[n for n in numbers if n > 1 for i in range(2)]
print(new_numbers_3)
new_numbers_4=[n > 1 for n in numbers if n * 2]
print(new_numbers_4)
