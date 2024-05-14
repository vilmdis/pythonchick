import re


class Book:

    def __init__(self, title:str, author:str, isbn:str, copies:int):
        self.title = title
        self.author = author
        self.__isbn = isbn
        self.copies = copies

    def check_availability(self):
        if bool(self.copies > 0):
            return 'Ok'
        else:
            return 'Not ok'

    def add_copies(self, num):
        if num > 0:
            self.copies += num
        else:
            print('Number can`t be <0.')

    def withdraw_copies(self, num):
        if num > 0 and num < self.copies:
            self.copies -= num
        else:
            print('Copies can`t be <0.')

    def get_isbn(self):
        return self.__isbn

    def validate_isbn(self):
        isbn = re.compile(r'^978-\d{1}+-\d{4}-\d{4}-\d{1}$')
        return bool(isbn.match(self.__isbn))


class User:

    def __init__(self, name:str, user_id:str):
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

    def take_books(self, book, num):
        if book.copies >= num and num > 0:
            book.copies -= num
            self.borrowed_books.append(book)
            return f'{self.get_name()} has borrowed {book.title}'
        else:
            return 'Sorry, we don`t have this book.'

    def give_away_books(self, book, num):
        if book in self.borrowed_books:
            book.copies += num
            self.borrowed_books.remove(book)
            return f'{self.get_name()} give away {book.title}'
        elif num <= 0:
            return 'Invalid number.'
        else:
            return 'You don`t have this book.'


class Employee(User, Book):

    def __init__(self, name, salary:int, library:list):
        super().__init__(name, user_id=None)
        self.__salary = salary
        self.library = library
        self.total_copies = 0

    def get_salary(self):
        return f'Your salary is {self.__salary}$.'

    def add_salary(self, num):
        if num > 0:
            self.__salary += num
            return f'Salary increased by {num}$'
        else:
            return 'Invalid number.'

    def reduce_salary(self, num):
        if num > 0 and num <= self.__salary:
            self.__salary -= num
            return f'Withdrawn {num}$ from salary.'
        else:
            return 'Invalid number.'

    def add_books(self, book):
        self.library.books.append(book)
        self.total_copies += 1
        return f'{book.title} added to the library.'

    def del_books(self, book):
        if book in self.library.books:
            self.library.books.remove(book)
            self.total_copies += 1
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

    def register_user(self, user):
        self.users.append(user)

    def search_books(self):
        for book in self.books:
            if book.get_isbn() == self.isbn:
                return book
        return None


library = Library()

book1 = Book("Harry Potter", "Rowling", "978-5-4675-2345-7", 5)
book2 = Book("The Great Gatsby", "Scott Fitzgerald", "978-0-7432-7356-5", 3)

customer1 = Customer("Vlad", 135235)
employee1 = Employee("Vadim", 3000, library)

employee1.add_books(book1)
employee1.add_books(book2)

library.register_user(customer1)
library.register_user(employee1)

print(book1.copies)
print(book2.copies)

book1.withdraw_copies(10)
book2.add_copies(10)

print(book1.check_availability())

print(employee1.total_copies)
print(book1.validate_isbn())
print(book1.get_isbn())

print(employee1.add_salary(500))

print(customer1.take_books(book1, 5))
print(employee1.del_books(book2))
print(customer1.give_away_books(book1, 7))

print(book1.copies)
print(book2.copies)
