class Book:
    def __init__(self, title, author, isbn, copies, total_copies):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.copies = copies
        self.total_copies = total_copies

    def check_availability(self, book):
        return isinstance(book, Book)

    def update_total_copies(self, num):
        if num > 0:
            self.total_copies += num
