x=10
y=5

def combos(x,y):
    combos=[]

    for x in range(0,x+1):
        for y in range(0,y+1):
            combos.append((x,y))
    return combos

all_combos=combos(x,y)
print(all_combos)

# El código de arriba esta lleno de shadows

# Es mejor expresarlo así:
x = 10
y = 5


print()

print('---Corrigiendo Shadows Name---\n')


def combos_2(input_x, input_y):
    _combos = []

    for _x in range(0, input_x + 1):
        for _y in range(0, input_y + 1):
            _combos.append((_x, _y))
    return _combos


all_combos = combos(x, y)
print(all_combos)
