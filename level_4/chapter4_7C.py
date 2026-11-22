class Location:
    def __init__(self,lat,long):
        self.lat=lat
        self.long=long
    def __repr__(self) -> str:
        return f'Location({self.lat},{self.long})'

    def __iter__(self):
        return iter((self.lat,self.long))

melbourne=Location(-37.840935,144.94645)
# No puedo hacer unpack falta el __iter__ TypeError: cannot unpack non-iterable Location object
# lat,long=melbourne


# ¿ Como lo resolvemos? => lo pasamos como argumentos ala función iter en forma de tupla, o sea hacemos unpacking en la clase
# Ahora sí me va a dejar
lat,long=melbourne
print(f'Latitud of Melbourne is : {lat} and Longitud is {long}')

# Ahora lo podemos pasar a una lista, sumarlos, es un iterable

# Otra forma muy común es con yield


class LocationTwo:
    def __init__(self, lat_two, long_two):
        self.lat_two = lat_two
        self.long_two = long_two

    def __repr__(self) -> str:
        return f"Location({self.lat_two},{self.long_two})"

    def __iter__(self):
        yield self.lat_two
        yield self.long_two
