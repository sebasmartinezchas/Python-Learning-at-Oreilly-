sample_books=[
    ("Digital Python","Eve Wilson","978-1-23456-789-0",199)
,
("Mastering AI","Frank Smith","978-1-23456-789-1",299),
("The Art of Programming","Grace Hopper","978-1-23456-789-2",399),
("Python for Beginners","Isaac Newton","978-1-23456-789-3",499),
("The Science of Computing","Albert Einstein","978-1-23456-789-4",599),
("The History of Python","Alan Turing","978-1-23456-789-5",699),
("The Future of Python","Nikola Tesla","978-1-23456-789-6",799),
("The Philosophy of Python","René Descartes","978-1-23456-789-7",899),
("The Economics of Python","Adam Smith","978-1-23456-789-8",999),
("The Politics of Python","Karl Marx","978-1-23456-789-9",1099),
("The Literature of Python","Virginia Woolf","978-1-23456-790-0",1199),
]

sample_ebooks=[
    ("Mastering AI","Frank Smith","978-1-23456-789-1",299,25.5),
    ("The Art of Programming","Grace Hopper","978-1-23456-789-2",399,35.5),
    ("Python for Beginners","Isaac Newton","978-1-23456-789-3",499,45.5),
    ("The Science of Computing","Albert Einstein","978-1-23456-789-4",599,55.5),
    ("The History of Python","Alan Turing","978-1-23456-789-5",699,65.5),
    ("The Future of Python","Nikola Tesla","978-1-23456-789-6",799,75.5),
    ("The Philosophy of Python","René Descartes","978-1-23456-789-7",899,85.5),
    ("The Economics of Python","Adam Smith","978-1-23456-789-8",999,95.5),
    ("The Politics of Python","Karl Marx","978-1-23456-789-9",1099,105.5),
    ("The Literature of Python","Virginia Woolf","978-1-23456-790-0",1199,115.5),
]

class Book:
    def __init__(self,title,author,isbn,price):
        self.title=title
        self.author=author
        self.isbn=isbn
        self.price=price
# Todo : Implement __str__ for user friendly display of book details
    def __str__(self):
        return f"{self.title} by {self.author} - ISBN: {self.isbn} - Price: {self.price}"
# Todo : Implement __repr__ for developer friendly display of book details
    def __repr__(self):
        return f"Book(title={self.title}, author={self.author}, isbn={self.isbn}, price={self.price})"
# Todo : Implement __eq__ for comparing books by ISBN
    def __eq__(self, other):
        if isinstance(other, Book):
            return self.isbn == other.isbn
        return False
# Todo : Implement __lt__ for comparing books by price
    def __lt__(self, other):
        if isinstance(other, Book):
            return self.price < other.price
        return False
# Todo : Implement __gt__ for comparing books by price
    def __gt__(self, other):
        if isinstance(other, Book):
            return self.price > other.price

class Ebook(Book):
    def __init__(self,title,author,isbn,price,size):
      # Todo Use Super to initialize the parent class
      super().__init__(title,author,isbn,price)
      self.size=size
      # Override the __str__ method to include ebook specific details(size)
    def __str__(self):
        return f"{super().__str__()} - Size: {self.size} MB"


books=[Book(*book) for book in sample_books]
ebooks=[Ebook(*ebook) for ebook in sample_ebooks]
all_media=books+ebooks
book_to_compare=Book("Mastering AI","Frank Smith","978-1-23456-789-1",299)
print("Books:")
for book in books:
    print(book)
print("\nEbooks:")
for ebook in ebooks:
    print(ebook)

print("User Friendly Output:")
for item in all_media:
    print(item)
print("\nDeveloper Friendly Output:")
for item in all_media:
    print(item)
print("\nComparing books:")
print(f"Book to compare: {book_to_compare}")
print(f"Is book_to_compare in books? {book_to_compare in books}")
print(f"Is book_to_compare in ebooks? {book_to_compare in ebooks}")
print(f"Is book_to_compare in all_media? {book_to_compare in all_media}")
print(f"Is book_to_compare equal to a book? {book_to_compare == books[0]}")
print(f"Is book_to_compare equal to an ebook? {book_to_compare == ebooks[0]}")