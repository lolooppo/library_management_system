"""
Author: Alaa Omran
Date: 2025-08-24
Description:
    This program implements a simple Library Management System with both backend and frontend layers.

    Features:
    - Add books and users to the system
    - Borrow and return books with validation
    - View library books and filter by prefix
    - Track which users borrowed specific books
    - Maintain borrowing limits based on book quantities

Structure:
    1. input_valid(): Utility function for validating user input
    2. Book class: Represents a book with borrowing and returning functionality
    3. User class: Represents a user and tracks borrowed books
    4. BackendManager class: Handles all data operations (books and users)
    5. FrontendManager class: Provides menu-driven UI for interacting with the system

Usage:
    Run the script and follow the menu prompts to manage books and users.
"""




def input_valid(msg, start, end):
    # Prompt user until they enter a numeric value within [start, end]
    while True:
        inp = input(msg)
        if not inp.isdecimal():
            print("Invalid Input..., Enter a numeric value.")
        elif not start <= int(inp) <= end:
            print("Invalid Range..., Try again!")
        else:
            return int(inp)



class Book:
    def __init__(self, name, id, total_quantity):
        self.name = name
        self.id = id
        self.total_quantity = total_quantity
        self.total_borrows = 0

    def borrow(self):
        if self.total_quantity - self.total_borrows == 0:
            return False
        self.total_borrows += 1
        return True

    def return_copy(self):
        if self.total_borrows == 0:
            return False
        self.total_borrows -= 1
        return True

    def __str__(self):
        return f'Book name: {self.name}\t\tBook id: {self.id}\t\ttotal_quantity: {self.total_quantity}\t\ttotal_borrows: {self.total_borrows}'

class User:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.borrowed_books = []

    def borrow(self, book):
        self.borrowed_books.append(book)

    def return_copy(self, borrowed_book):
        for idx, book in enumerate(self.borrowed_books):
            if book.id == borrowed_book.id:
                del self.borrowed_books[book.id - 1]
                break

    def is_borrowed(self, borrowed_book):
        for book in self.borrowed_books:
            if book.id == borrowed_book.id:
                return True
        return False

    def __str__(self):
        return f'user name: {self.name}\t\tid: {self.id}'



class BackendManager:
    def __init__(self):
        self.books = []
        self.users = []

    def add_book(self, name, id, total_quantity):
        self.books.append(Book(name, id, total_quantity))

    def add_user(self, name, id):
        self.users.append(User(name, id))

    def get_user_by_name(self, user_name):
        for user in self.users:
            if user.name == user_name:
                return user
        return None

    def get_book_by_name(self, book_name):
        for book in self.books:
            if book.name == book_name:
                return book
        return None

    def borrow_book(self, user_name, book_name):
        user = self.get_user_by_name(user_name)
        book = self.get_book_by_name(book_name)

        if user is None or book is None:
            return False

        if book.borrow():
            user.borrow(book)
            return True
        return False

    def return_book(self, user_name, book_name):
        user = self.get_user_by_name(user_name)
        book = self.get_book_by_name(book_name)

        if user is None or book is None:
            return False

        if user.is_borrowed(book):
            user.return_copy(book)
            book.return_copy()
            return True

        return False

    def get_users_borrowed_book(self, book_name):
        book = self.get_book_by_name(book_name)
        if book is None:
            return []

        return [user.name for user in self.users if user.is_borrowed(book)]

    def get_books_with_prefix(self, prefix):
        return [book for book in self.books if book.name.startswith(prefix)]



class FrontendManager:
    def __init__(self):
        self.backend = BackendManager()
        self.add_dummy_data()

    def print_options(self):
        print('Program options:')

        menu = [
            'Add book',
            'Print library books',
            'Print books by prefix',
            'Add user',
            'Borrow book',
            'Return book',
            'Print users borrowed book',
            'Print users',
        ]

        messages = [f'{idx + 1}) {msg}' for idx, msg in enumerate(menu)]
        print('\n'.join(messages))

        return input_valid(f'Enter your choice from (1 to {len(messages)}): ', 1, len(messages))

    def add_dummy_data(self):
        self.backend.add_book('math4', '100', 3)
        self.backend.add_book('math2', '101', 5)
        self.backend.add_book('math1', '102', 4)
        self.backend.add_book('math3', '103', 2)
        self.backend.add_book('prog1', '201', 3)
        self.backend.add_book('prog2', '202', 3)

        self.backend.add_user('mostafa', '30301')
        self.backend.add_user('ali', '50501')
        self.backend.add_user('noha', '70701')
        self.backend.add_user('ashraf', '90901')

        self.backend.borrow_book('mostafa', 'math3')
        self.backend.borrow_book('noha', 'math3')

    def run(self):
        while True:
            choice = self.print_options()
            if choice == 1:
                self.add_book()
            elif choice == 2:
                self.print_library_books()
            elif choice == 3:
                self.print_name_prefix()
            elif choice == 4:
                self.add_user()
            elif choice == 5:
                self.borrow_book()
            elif choice == 6:
                self.return_book()
            elif choice == 7:
                self.print_users_borrowed_book()
            elif choice == 8:
                self.print_users()
            else:
                break

    def add_book(self):
        print('Enter book info: ')
        book_name = input('Book name: ')
        book_id   = input('Book id: ')
        total_quantity = int(input('Total quantity: '))
        self.backend.add_book(book_name, book_id, total_quantity)

    def print_name_prefix(self, just_print_all = False):
        prefix = ''
        if not just_print_all:
            prefix = input('Enter book name prefix: ')

        books = self.backend.get_books_with_prefix(prefix)
        books_str = '\n'.join([str(book) for book in books])
        print(books_str)

    def print_library_books(self):
        self.print_name_prefix(just_print_all = True)

    def add_user(self):
        print('Enter user info: ')
        user_name = input('User name: ')
        user_id = input('User id: ')
        self.backend.add_user(user_name, user_id)

    def read_user_name_and_book_name(self, trials = 3):
        """
        The function tries to read valid user name and password up to #trials
        If finally correct, it returns the read names, otherwise None, None
        """
        trials += 1

        while trials > 0:
            trials -= 1
            print('Enter user name and book name')

            user_name = input('User name: ')
            if self.backend.get_user_by_name(user_name) is None:
                print('Invalid user name!')
                continue

            book_name = input('Book name: ')
            if self.backend.get_book_by_name(book_name) is None:
                print('Invalid book name!')
                continue

            return user_name, book_name

        print('You did several trials! Try later.')
        return None, None

    def borrow_book(self):
        user_name, book_name = self.read_user_name_and_book_name()

        if user_name is None or book_name is None:
            return

        if not self.backend.borrow_book(user_name, book_name):
            print('Failed to borrow the book!')

    def return_book(self):
        user_name, book_name = self.read_user_name_and_book_name()
        if user_name is None or book_name is None:
            print('No such book or user')
            return

        if not self.backend.return_book(user_name, book_name):
            print('This user did not borrow this book!')
        else:
            print('Book returned successfully!')


    def print_users_borrowed_book(self):
        book_name = input('Book name: ')
        if self.backend.get_book_by_name(book_name) is None:
            print('Invalid book name!')
        else:
            users_lst = self.backend.get_users_borrowed_book(book_name)

            if not users_lst:
                print('\nNo one borrowed this book')
            else:
                print('\nList of users borrowed this book')
                for user in users_lst:
                    print(user)

    def print_users(self):
        users_str = '\n'.join([str(user) for user in self.backend.users])
        print(users_str)


if __name__ == '__main__':
    system = FrontendManager()
    system.run()