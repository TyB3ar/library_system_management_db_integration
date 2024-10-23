# module for Authors class and methods
from database import Database
import mysql.connector
import re 


class Author: # A class representing book authors with attributes like name and biography.
    def __init__(self): 
        self.library = Database(database='', password='', user='', host='')
        
      
    def check_name(self, name): # validate if user enters a name 
        regex = r'^[A-Za-z\s.]+$'    # checks for '.' and ' ' in name as well 
        if re.match(regex, name):
            return True
        else:
            return False 
    
    def author_in_library(self, author_name): # method to validate if author in library COMPLETE    
        try:
            self.library.connect()   # connect to db 
                   
            query = "SELECT COUNT(*) FROM authors WHERE name LIKE %s" # query and execute to count occurrence of name in db 
            self.library.cursor.execute(query, (author_name,))   
         
            find_name = self.library.cursor.fetchone()  
            if find_name[0] > 0:  # if there is a count
                fetch_name = "SELECT * FROM authors WHERE name LIKE %s"  # query to find name of author from table
                self.library.cursor.execute(fetch_name, (author_name,))  
                found_name = self.library.cursor.fetchone()   # value name and bio to 'found_name' 
                self.library.close()
                return True # Returns true if author name is found in library
            else:            
                self.library.close()
                return False  # returns false if author name is not found in library 
        except Exception as e:
            print(f"Error: {e}") 
            
            
    def new_author(self):   # method to add author COMPLETE
        try: 
            while True:              
                new_name = input("Enter Author Name: ")
                if self.check_name(new_name): # validate name input 
                    new_bio = input("Enter a short biography about the author: ")  
                    if self.author_in_library(new_name):
                        break 
                    else:
                        new_author = (new_name, new_bio)
                        add_author = "INSERT INTO authors(name, biography) VALUES(%s, %s)"
                        self.library.execute_query(add_author, new_author)
                        self.library.close()                    
                        print(f"{new_name} was added to authors.")                   
                        break 
                else:
                    print("Invalid Name.")
        except Exception as e:
            print(f"Error: {e}") 
        
     
    def view_author(self):  # method to search and view details of particular author COMPLETE
        try: 
            while True:
                author_name = input("Enter the name of the author you wish to view: ")
                if self.check_name(author_name):  # validate if input is possible name of author
                    self.library.connect()   # connect to db 
                   
                    query = "SELECT COUNT(*) FROM authors WHERE name LIKE %s" 
                    self.library.cursor.execute(query, (author_name,))   # query and execute to count occurrence of name in db 
         
                    find_name = self.library.cursor.fetchone()  
                    if find_name[0] > 0:  # if there is a count
                        fetch_name = "SELECT * FROM authors WHERE name LIKE %s"  # query to find name of author from table
                        self.library.cursor.execute(fetch_name, (author_name,))  
                        found_name = self.library.cursor.fetchone()   # value name and bio to 'found_name' 
                        print(f"Author found as :\nAUTHOR ID: {found_name[0]} - NAME: {found_name[1]} - BIOGRAPHY: {found_name[2]}")
                        self.library.close()
                        break 
                    else:  # else if author is not found in db
                        print("Author not found.")            
                        self.library.close()
                        break 
                else:
                    print("Invalid Name.")
         
        except Exception as e:
            print(f"Error: {e}") 


    def display_authors(self):  # method to display all authors and bios COMPLETE
        try: 
            print("Current Authors in library: ")
            self.library.connect()
            authors = self.library.fetch_all("SELECT * FROM authors", )
            for author in authors:
                author_display = f"AUTHOR ID: {author[0]} - NAME: {author[1]} - BIOGRAPHY: {author[2]}" 
                print(author_display)  
            self.library.close() 
         
        except Exception as e:
            print(f"Error: {e}")  
