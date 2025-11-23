# Library Management System
# Created by: Ayush Kumar
# Class: B.Tech CSE (DS) | Roll No: 2501420003 | Date: 22/11/2025

from typing import Optional


class Book:
    def __init__(self, title: str, author: str, isbn: str, status: str = "available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def to_line(self) -> str:
        # replace newlines/commas in fields to avoid corrupting the file format
        t = self.title.replace("\n", " ").replace(",", " ")
        a = self.author.replace("\n", " ").replace(",", " ")
        return f"{t},{a},{self.isbn},{self.status}\n"

    @staticmethod
    def from_line(line: str) -> Optional["Book"]:
        parts = [p.strip() for p in line.strip().split(",")]
        if len(parts) < 4:
            return None
        title, author, isbn, status = parts[0], parts[1], parts[2], parts[3]
        return Book(title, author, isbn, status)

    def __str__(self) -> str:
        return f"{self.title} | {self.author} | {self.isbn} | {self.status}"


class LibraryInventory:
    def __init__(self, filename: str = "books.txt"):
        self.filename = filename
        self.books: list[Book] = []
        self.load_books()

    def load_books(self) -> None:
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                for line in f:
                    book = Book.from_line(line)
                    if book:
                        self.books.append(book)
        except FileNotFoundError:
            # start with empty library (file will be created on first save)
            print("File not found! Starting with an empty library.")

    def save_books(self) -> None:
        with open(self.filename, "w", encoding="utf-8") as f:
            for book in self.books:
                f.write(book.to_line())

    def add_book(self, book: Book) -> bool:
        # enforce unique ISBN
        if self.search_by_isbn(book.isbn):
            return False
        self.books.append(book)
        self.save_books()
        return True

    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        lookup = isbn.strip()
        for book in self.books:
            if book.isbn.strip() == lookup:
                return book
        return None

    def display_all(self) -> None:
        if not self.books:
            print("No books in the library.")
            return
        print("\nTitle | Author | ISBN | Status")
        print("-" * 50)
        for book in self.books:
            print(book)


def menu() -> None:
    inventory = LibraryInventory()

    try:
        while True:
            print("\n===== Library Menu =====")
            print("1. Add Book")
            print("2. Issue Book")
            print("3. Return Book")
            print("4. View All Books")
            print("5. Exit")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                title = input("Enter title: ").strip()
                author = input("Enter author: ").strip()
                isbn = input("Enter ISBN: ").strip()

                if not title or not author or not isbn:
                    print("Title, author and ISBN cannot be empty.")
                    continue

                new_book = Book(title, author, isbn)
                if inventory.add_book(new_book):
                    print("Book added!")
                else:
                    print("A book with that ISBN already exists.")

            elif choice == "2":
                isbn = input("Enter ISBN to issue: ").strip()
                book = inventory.search_by_isbn(isbn)
                if book:
                    if book.status == "available":
                        book.status = "issued"
                        inventory.save_books()
                        print("Book issued!")
                    else:
                        print("Book already issued.")
                else:
                    print("Book not found.")

            elif choice == "3":
                isbn = input("Enter ISBN to return: ").strip()
                book = inventory.search_by_isbn(isbn)
                if book:
                    if book.status == "issued":
                        book.status = "available"
                        inventory.save_books()
                        print("Book returned!")
                    else:
                        print("Book is already available.")
                else:
                    print("Book not found.")

            elif choice == "4":
                inventory.display_all()

            elif choice == "5":
                print("Exiting...")
                break

            else:
                print("Invalid choice!")

    except KeyboardInterrupt:
        print("\nExiting (keyboard interrupt).")


if __name__ == "__main__":
    menu()
