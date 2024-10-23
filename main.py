# main module for running and testing application
from database import Database
from books import Book 
from users import User
from authors import Author

def main_menu(): # main function for ui for user to chose what to do 
    print("Welcome to the Library Management System with Database Integration!")   
    try:
        books = Book() 
        user = User()
        author = Author()
        while True:
            print("\nMain Menu:\n 1. Book Operations\n 2. User Operations\n 3. Author Operations\n 4. Exit") # main menu
            first_choice = input('Please enter the number of the operation you wish to perform: ') # input for main menu option 
            
            if first_choice == '1': # Book Operations
                while True: 
                    print("\nBook Operations:\n 1. Add a new book\n 2. Borrow a book\n 3. Return a book\n 4. Search for a book\n 5. Display all Books\n 6. Return to Main Menu") 
                    book_choice = input("Please enter the number of the operation you wish to perform: ")   # user choice for book operation
                
                    if book_choice == '1': # Add a new book
                        books.add_book()         
                    elif book_choice == '2': # Borrow a book 
                        books.borrow_book() 
                    elif book_choice == '3': # Return a book
                        books.return_book() 
                    elif book_choice == '4': # Search for a book
                        books.search_book()  
                    elif book_choice == '5': # Display all books 
                        books.display_books()     
                    elif book_choice == '6': # Return to main menu
                        break
                    else:
                        print("Error, invalid choice.")
            elif first_choice == '2': # User Operations
                while True:
                    print("\nUser Operations:\n 1. Add a new User\n 2. View User Details\n 3. Display all users\n 4. Return to Main Menu") 
                    user_choice = input("Please enter the number of the operation you wish to perform: ") # user input for user operations
                
                    if user_choice == '1': # Add a new user
                        user.add_user() 
                    elif user_choice == '2': # View User Details 
                        user.view_user()  
                    elif user_choice == '3': # Display all users
                        user.display_users()  
                    elif user_choice == '4': # Return to main menu
                        break 
                    else:
                        print("Error, invalid choice.") 
            elif first_choice == '3': # Author Operations
                while True:
                    print("\nAuthor Operations:\n 1. Add a new author\n 2. View Author Details\n 3. Display All Authors\n 4. Return to Main Menu")
                    author_choice = input("Please enter the number of the operation you wish to perform: ")
                
                    if author_choice == '1': # Add a New Author 
                        author.new_author() 
                    elif author_choice == '2': # View Author Details DONE 
                        author.view_author() 
                    elif author_choice == '3': # Display All Authors DONE
                        author.display_authors()  
                    elif author_choice == '4': # Return to Main Menu DONE 
                        break
                    else:
                        print("Error, invalid input.")  
            elif first_choice == '4': # Exit 
                print("\nThank you, have a great rest of your day!")
                break
            else: # if input is anything other than 1, 2, 3, 4
                print("Error, invalid choice.")             
    except Exception as e:
        print(f"Error: {e}")

main_menu() 
