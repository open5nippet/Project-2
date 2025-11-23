# Library Management System
# Created by:-
# Name- Ayush Kumar
# Class- Btech CSE (DS)
# Roll No- 2501420003
# Date- 22/11/25

class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title= title
        self.author= author
        self.isbn= isbn
        self.status= status

    def to_line(self):
        return f"{self.title},{self.author},{self.isbn},{self.status}\n"

    def from_line(line):
        title, author, isbn, status = line.strip().split(",")
        return Book(title, author, isbn, status)


class LibraryInventory:
    def __init__(self, filename="books.txt"):
        self.filename= filename
        self.books= []
        self.load_books()

    def load_books(self):
        try:
            with open(self.filename, "r") as f:
                for line in f:
                    self.books.append(Book.from_line(line))
        except FileNotFoundError:
            print("File not found! Starting with an empty library.")

    def save_books(self):
        with open(self.filename, "w") as f:
            for book in self.books:
                f.write(book.to_line())

    def add_book(self, book):
        self.books.append(book)
        self.save_books()

    def search_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn==isbn:
                return book
        return None

    def display_all(self):
        for book in self.books:
            print(f"{book.title} | {book.author} | {book.isbn} | {book.status}")


def menu():
    inventory= LibraryInventory()

    while True:
        print("\n===== Library Menu =====")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice=="1":
            title= input("Enter title: ")
            author= input("Enter author: ")
            isbn= input("Enter ISBN: ")

            book= Book(title, author, isbn)
            inventory.add_book(book)
            print("Book added!")

        elif choice=="2":
            isbn= input("Enter ISBN: ")
            book= inventory.search_by_isbn(isbn)
            if book:
                if book.status=="available":
                    book.status= "issued"
                    inventory.save_books()
                    print("Book issued!")
                else:
                    print("Book already issued")
            else:
                print("Book not found")

        elif choice=="3":
            isbn= input("Enter ISBN: ")
            book= inventory.search_by_isbn(isbn)
            if book:
                if book.status=="issued":
                    book.status= "available"
                    inventory.save_books()
                    print("Book returned!")
                else:
                    print("Book already available.")
            else:
                print("Book not found.")

        elif choice=="4":
            inventory.display_all()

        elif choice=="5":
            print("Exiting...")
            break

        else:
            print("Invalid choice!")

menu()