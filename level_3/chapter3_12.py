# Apply Duck Typing in Python / Adding Flexibility with Duck Typing
# Exercice => Create a third class called Webservice
# so that it can be called by the process_resource function
class Duck:
    def __init__(self, name) -> None:
        self.name = name

    def quack(self):
        print("Quack")


class Person:
    def __init__(self, name, occupation):
        self.name = name
        self.occupation = occupation

    def quack(self):
        print("Ahem, Quack!")


duck_imposter = Person("Carl", "Animal Sound Artist")
duck_imposter.quack()

print("------ List prints -----")
ducks = [Duck("Webby"), Person("Carl", "Animal Sound Artist")]

for duck in ducks:
    duck.quack()


# Another exampl
print("--- Database Example---")


class TextFile:
    def read(self):
        print("Reading from a text file.")

    def close(self):
        print("Closing the text file.")


class Database:
    def read(self):
        print("Reading from a database.")

    def close(self):
        print("Closing the database. ")


class WebService:
    def read(self):
        print("Reading from a web service.")

    def close(self):
        print("Closing the webservice.")


def process_resource(resource):
    resource.read()
    resource.close()


text_file = TextFile()
db = Database()
ws = WebService()
process_resource(text_file)
process_resource(db)
process_resource(ws)
