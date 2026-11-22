# Use Slots to Create Memory-Efficient Python Classes / Restricting Class Attributes with slots
class Point:
    __slots__=('x','y','z')
    def __init__(self, x, y, z):
        self.x, self.y, self.z = (x, y, z)


def point_path_from_file(filename):
    with open(filename) as lines:
        return [Point(*map(float, point_line.split())) for point_line in lines]

p=Point(1,2,3)

print(p.__dict__)
print(p.x)


class Player:
    __slots__=('username','level')
    def __init__(self,username,level):
        self.username=username
        self.level=level

player=Player('gamer1',5)
