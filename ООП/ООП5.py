import re


class Book:

    def __init__(self, title, author, isbn, copies, total_copies):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.copies = copies
        self.total_copies = total_copies

    def check_availability(self):
        return self.copies > 0

    def update_total_copies(self, num):
        if num > 0:
            self.total_copies = num
        else:
            return 'Total copies can`t be <0.'

    def update_copies(self, num):
        if num > 0:
            self.copies = num
        else:
            return 'Copies can`t be <0.'

    def validate_isbn(self):
        isbn = re.compile(r'^978-\d{1}+-\d{4}-\d{4}-\d{1}$')
        return bool(isbn.match(self.isbn))

    def get_isbn(self):
        return self.isbn


class User:

    def __init__(self, name, user_id):
        self._name = name
        self._user_id = user_id

    def get_name(self):
        return f'Your name is {self._name}'

    def get_id(self):
        return f'Your id is {self._user_id}'


class Customer(User):

    def __init__(self, name, user_id):
        super().__init__(name, user_id)
        self.borrowed_books = []

    def get_name(self):
        return super().get_name()

    def get_id(self):
        return super().get_id()

    def take_books(self, book):
        if book.check_availability():
            book.update_copies(book.copies - 1)
            self.borrowed_books.append(book)
            return f'{self.get_name()} has borrowed {book.title}'
        else:
            return 'Sorry, we don`t have this book.'

    def give_away_books(self, book):
        if book in self.borrowed_books:
            book.update_copies(book.copies + 1)
            return self.borrowed_books.pop(book)
        else:
            return 'You don`t have this book.'


class Employee(User):

    def __init__(self, name, salary, library):
        super().__init__(name, user_id=None)
        self.__salary = int(salary)
        self.library = library

    def get_name(self):
        return super().get_name()

    def get_salary(self):
        return f'Your salary is {self.__salary}$.'

    def add_salary(self, num):
        if num > 0:
            self.__salary += num
            return f'Salary increased by {num}$'
        else:
            return 'Invalid number.'

    def withdraw_salary(self, num):
        if num > 0 and num <= self.__salary:
            self.__salary -= num
            return f'Withdrawn {num}$ from salary.'
        else:
            return 'Invalid number.'

    def add_books(self, book):
        book.update_total_copies(book.total_copies + book.copies)
        self.library.books.append(book)
        return f'{book.title} added to the library.'

    def del_books(self, book):
        if book in self.library.books:
            book.update_total_copies(book.total_copies - book.copies)
            self.library.books.remove(book)
            return f'{book.title} removed from the library.'
        else:
            return 'This book isn`t in the library.'


class Library:

    def __init__(self):
        self.books = []
        self.users = []

    def show_all_users(self):
        return self.users

    def show_all_books(self):
        return self.books

    def verify_user(self, user):
        self.users.append(user)

    def search_books(self):
        for book in self.books:
            if book.get_isbn() == self.isbn:
                return book
        return None


library = Library()

book1 = Book("Harry Potter", "Rowling", "978-5-4675-2345-7", 5, 10)
book2 = Book("The Great Gatsby", "Scott Fitzgerald", "978-0-7432-7356-5", 3, 11)

customer1 = Customer("Vlad", 135235)
employee1 = Employee("Vadim", 3000, library)

employee1.add_books(book1)
employee1.add_books(book2)

library.verify_user(customer1)
library.verify_user(employee1)

print(book1.check_availability())
book1.update_copies(4)
print(book1.total_copies)
print(book1.validate_isbn())
print(book1.get_isbn())

print(employee1.add_salary(500))

print(customer1.take_books(book1))
print(employee1.del_books(book2))
print(customer1.give_away_books(book2))
