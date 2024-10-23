# module for Books class and methods
from database import Database
import mysql.connector
from users import User
from authors import Author
import re 
from datetime import datetime
from datetime import timedelta
from datetime import date 


class Book: # A class representing individual books with attributes such as title, author,  genre, publication date, and availability status.
    def __init__(self): 
        self.library = Database(database='', password='', user='', host='')

        
    def book_in_library(self, title):  # method to validate if book title already in library 
        try:
            self.library.connect()   # connect to db 
            query = "SELECT COUNT(*) FROM books WHERE title LIKE %s" 
            self.library.cursor.execute(query, (title,))   # query and execute to count occurrence of title in books     
            find_book = self.library.cursor.fetchone()  
            if find_book[0] > 0:  # if there is a count
                return True  # return True if title is found in library 
                self.library.close()
            else:
                return False # return false if title not found
                self.library.close() 
        except Exception as e:
            print(f"Error: {e}") 
 
 
    def check_isbn(self, isbn_num):  # method to validate isbn number
        try:
            regex = r'^\d{13}$'   # regex to validate ISBN 10 number 
            if re.match(regex, isbn_num): # checks if library id is alphanumerical, between 3-10 characters 
                return True
            else:
                return False
        except Exception as e:
            print(f"Error: {e}")
  
            
    def check_date(self, pub_date):  # method to validate date input 
        regex = r'^\d{4}-\d{2}-\d{2}$'
        if re.match(regex, pub_date):
            return True
        else:
            return False 
    
         
    def add_book(self): # add a book to library COMPLETE    
        try:
            while True: 
                # user enters input to add book to db : (Title, Author Name, ISBN, Pub_Date, Set available to 1) 
                new_title = input("Enter the Title of the book: ")
                
                # Validate Book title is new:
                if self.book_in_library(new_title):  # if book title is in library
                    print("Title already found in library.") 
                    break 
                else:   # if title is new 
                    new_book_author = input("Enter name of author: ") 
                    
                    if Author.author_in_library(self, new_book_author): # if author is already in Library, retireive info for ID
                        self.library.connect()
                        show_author = 'SELECT a.id AS AuthorID, a.name AS Name FROM authors a WHERE name LIKE %s'
                        self.library.cursor.execute(show_author, (new_book_author,))
                        author_info = self.library.cursor.fetchone() 
                        print("Author found in Library as (AuthorID, Name): ")
                        print(author_info) 
                        author_id = input("Enter Author ID of author: ")
                        self.library.close() 
                    else:
                        # add author to library 
                        new_bio = input("Author not found in Library. Please enter a short biography about the author: ") 
                        self.library.connect() 
                        new_author = (new_book_author, new_bio)
                        add_author = "INSERT INTO authors(name, biography) VALUES(%s, %s)"
                        self.library.execute_query(add_author, new_author)
                        self.library.close()                    
                        print(f"{new_name} was added to authors.") 
                        
                        # Now retrieve info for author id:
                        if Author.author_in_library(self, new_book_author): # if author is already in Library, retireive info for ID
                            self.library.connect()
                            show_author = 'SELECT a.id AS AuthorID, a.name AS Name FROM authors a WHERE name LIKE %s'
                            self.library.cursor.execute(show_author, (new_book_author,))
                            author_info = self.library.cursor.fetchone() 
                            print("Author found in Library as (AuthorID, Name): ")
                            print(author_info) 
                            author_id = input("Enter Author ID of author: ")
                            self.library.close()
                        
                    new_isbn = input("Enter the ISBN of the book: ")                    
                    if self.check_isbn(new_isbn):  # validate isbn  number input 
                        new_pub_date = input("Enter the publication date(year-month-date): ")
                        
                        if self.check_date(new_pub_date): # validate date input 
                            # Now, we add everything for new book into Books table in db 
                            self.library.connect() 
                            add_book = "INSERT INTO books(title, author_id, isbn, publication_date, availability) VALUES(%s, %s, %s, %s, DEFAULT)"
                            self.library.execute_query(add_book, (new_title, author_id, new_isbn, new_pub_date)) 
                            self.library.close()
                            print(f"'{new_title}' added to library.")
                            break 
                        else:
                            print("Invalid Date Entry") 
                    else:
                        print("Invalid ISBN number")                 
                        
        except Exception as e:
            print(f"Error: {e}") 

    
    def borrow_book(self): # borrow book from library COMPLETE     
        try:
            # Input book title to borrow, Input user_id, input borrow date, make return date 7 days later, add book id(from title) and user id to 'borrowed_books' 
            while True:
                book_title = input('Enter the title of the book you wish to borrow: ') # user input title of book to borrow
                
                if self.book_in_library(book_title): # check if title is in library first 
                    # retirieve book id:
                    self.library.connect() 
                    book_info = 'SELECT b.id AS BookID, b.title AS BookTitle FROM books b WHERE title LIKE %s' 
                    self.library.cursor.execute(book_info, (book_title,)) 
                    print_book = self.library.cursor.fetchone() 
                    print(f"{book_title} found in library as: {print_book}")
                    self.library.close() 
                    
                    book_id = input("Enter the Book ID listed above: ") 
                    
                    library_id = input("Enter the Library ID of user to borrow: ") 
                    
                    if User.user_is_active(self, library_id):   # if user_id is found in db
                        # Retrieve User ID from Library ID
                        self.library.connect()
                        fetch_user = "SELECT u.id AS UserID, u.library_id AS LibraryID FROM users u WHERE library_id LIKE %s" 
                        self.library.cursor.execute(fetch_user, (library_id,)) 
                        user_info = self.library.cursor.fetchone() 
                        print(f"User found as: {user_info}")
                        self.library.close()
                        
                        user_id = input("Enter the User ID as listed above: ")  
                        
                        borrow_date = input("Enter today's date(year-month-day): ") 
                        
                        if self.check_date(borrow_date):
                            b_date = datetime.strptime(borrow_date, "%Y-%m-%d")  # set input date to datetime object 
                            r_date = b_date + timedelta(days=7)  # set return date to exactly 7 days after borrow date    
                            return_date = r_date.strftime("%Y-%m-%d")  # convert return date to string 
                                                 
                            # add info to 'borrowed books' table in db: 
                            borrowing_book = (user_id, book_id, borrow_date, return_date)
                            self.library.connect() 
                            add_borrowed_book = "INSERT INTO borrowed_books(user_id, book_id, borrow_date, return_date) VALUES(%s, %s, %s, %s)"
                            self.library.execute_query(add_borrowed_book, borrowing_book) 
                            self.library.close() 
                            print(f"{book_title} is now being borrowed by user: {user_id}") 
                            
                            # Change default value of 'availability' in books: 
                            self.library.connect() 
                            change_availability = "UPDATE books SET availability = '0' WHERE id = %s"
                            self.library.execute_query(change_availability, (book_id,)) 
                            self.library.close() 
                             
                            break 
                                                
                        else:
                            print("Invalid date") 
                    else:
                        print("Invalid User ID")  
                else:   # if not in library, print statement book wasn't found 
                    print("Sorry, but that title was not found.") 
        
        except Exception as e:
            print(f"Error: {e}")  
       
                    
    def return_book(self): # method to return used books COMPLETE
        try:
            # input borrowed book_id(title) and user_id from 'borrowed_books', remove from table if in 'borrowed_books', reset 'availability' to default 
            while True:
                book_title = input("Enter Title of book to return: ")
                if self.book_in_library(book_title):
                    # retirieve book id:
                    self.library.connect() 
                    book_info = 'SELECT b.id AS BookID, b.title AS BookTitle FROM books b WHERE title LIKE %s' 
                    self.library.cursor.execute(book_info, (book_title,)) 
                    print_book = self.library.cursor.fetchone() 
                    print(f"{book_title} found in library as: {print_book}")
                    self.library.close() 
                    
                    book_id = input("Enter the Book ID listed above: ")                     
                    # retirieve info from 'borrowed_books' 
                    self.library.connect() 
                    borrowed_book_info = 'SELECT * FROM borrowed_books WHERE book_id LIKE %s' 
                    self.library.cursor.execute(borrowed_book_info, (book_id,)) 
                    print_book = self.library.cursor.fetchone() 
                    print(f"Borrowed book found:\n UserID - {print_book[1]}, BookID - {print_book[2]}") 
                    self.library.close() 
                    
                    # Once info is retrieved, remove from 'borrowed_books', or return the book 
                    self.library.connect()
                    borrow_id = print_book[0]                    
                    return_book = "DELETE FROM borrowed_books WHERE id = %s"
                    book_returned = self.library.execute_query(return_book, (borrow_id,)) 
                    self.library.close() 
                    
                    print(f"{book_title} has been returned.")
                    
                    # Reset book to 'available
                    self.library.connect()
                    change_availability = "UPDATE books SET availability = '1' WHERE id = %s"
                    self.library.execute_query(change_availability, (book_id,))    
                    self.library.close()
                    break     
                    
                else:
                    print("Book not found.") 
        
        except Exception as e:
            print(f"Error: {e}") 
            
    
    def search_book(self): # Search for book by title COMPLETE 
        try:
            while True:
                book_title = input("Enter the title of the book you wish to find: ") 
                self.library.connect() # connect to db               
                find_book = "SELECT COUNT(*) FROM books WHERE title LIKE %s"   # search for title in db - books table 
                self.library.cursor.execute(find_book, (book_title,)) #                
                found_book = self.library.cursor.fetchone()
                if found_book[0] > 0:
                    fetch_book = "SELECT * FROM books WHERE title LIKE %s" 
                    self.library.cursor.execute(fetch_book, (book_title,)) 
                    book_found = self.library.cursor.fetchone()
                    availability = "Available" if book_found[5] == '1' else "Unavailable"  # Index for 'Availability'
                    print(f"Book found as:\nBOOK ID: {book_found[0]} - TITLE: {book_found[1]} - AUTHOR ID: {book_found[2]} - ISBN: {book_found[3]} - PUBLISH DATE: {book_found[4]} - {availability}")
                    self.library.close()
                    break 
                else:
                    print("Book not found in library")
                    self.library.close()
                    break 
                        
        except Exception as e:
            print(f"Error: {e}")
    
    
    def display_books(self): # display all books and status COMPLETE
        try:
            print("\nCurrent books in library:")
            self.library.connect()
            books = self.library.fetch_all(
            "SELECT b.id AS BookID, b.title AS BookTitle, b.author_id AS AuthorID, b.isbn AS ISBN, b.publication_date AS PublishDate, b.availability AS Availability FROM books b")
            for book in books:
                availability = "Available" if book[5] == '1' else "Unavailable"  # Index for 'Availability'
                book_display = f"BOOK ID: {book[0]} - TITLE: {book[1]} - AUTHOR ID: {book[2]} - ISBN: {book[3]} - PUBLISH DATE: {book[4]} - {availability}"
                print(book_display)
                self.library.close()
        except Exception as e:
            print(f"Error: {e}")

