# Module for User class and methods  
from database import Database
import mysql.connector
import re 

class User: # A class to represent library users with attributes like name, library ID, and a list of borrowed book titles.
    def __init__(self):
        self.library = Database(database='', password='', user='', host='')
       

        
    def check_library_id(self, library_id): # method to validate library id input
        regex = r"^[A-Za-z]\w{3,10}$" 
        if re.match(regex, library_id): # checks if library id is alphanumerical, between 3-10 characters 
            return True
        else:
            return False
    
    
    def user_is_active(self, library_id):  # method to validate if user_id exists in db (is active) 
        self.library.connect() 
        find_user = "SELECT COUNT(*) FROM users WHERE library_id LIKE %s"
        self.library.cursor.execute(find_user, (library_id,)) 
        user_info = self.library.cursor.fetchone() 
        if user_info[0] > 0:   # return True if user_id is found in db 
            return True
            self.library.close() 
        else:   # return False if user_id is not found in db 
            return False
            self.library.close()

    
    def add_user(self): #  method to add new user to 'users' table from db COMPLETE
        try:
            while True:
                new_username = input("Enter name for new user: ") 
                new_lib_id = input("Enter new library ID: ")
                if self.check_library_id(new_lib_id):  # validate username 
                    self.library.connect()
                    
                    user_query = "SELECT COUNT(*) FROM users WHERE library_id LIKE %s"  # validate user is not already in library
                    self.library.cursor.execute(user_query, (new_lib_id,))
                    find_user = self.library.cursor.fetchone()
                    if find_user[0] > 0:
                        print("User already in library.")
                        self.library.close()
                        break
                    else:
                        add_user = "INSERT INTO users(name, library_id) VALUES(%s, %s)"
                        self.library.execute_query(add_user, (new_username, new_lib_id)) 
                        self.library.close()
                        print(f"New user {new_username} added to users.")
                        break 
                else:
                    print("Invalid Username")
        except Exception as e:
            print(f"Error: {e}")
            
                  
    def view_user(self):  # method to view particular user COMPLETE
        try: 
            while True:
                user_id = input("Enter the Library ID of the user you wish to view: ")
                if self.check_library_id(user_id):  # validate if input is possible name of author
                    self.library.connect()   # connect to db 
                   
                    query = "SELECT COUNT(*) FROM users WHERE library_id LIKE %s" 
                    self.library.cursor.execute(query, (user_id,))   # query and execute to count occurrence of name in db 
         
                    find_name = self.library.cursor.fetchone()  
                    if find_name[0] > 0:  # if there is a count
                        fetch_name = "SELECT * FROM users WHERE library_id LIKE %s"  # query to find name of author from table
                        self.library.cursor.execute(fetch_name, (user_id,))  
                        found_name = self.library.cursor.fetchone()   # value name and bio to 'found_name' 
                        print("User found: ")
                        print(found_name) 
                        self.library.close()
                        break 
                    else:  # else if author is not found in db
                        print("User not found.")            
                        self.library.close()
                        break 
                else:
                    print("Invalid Name.")
         
        except Exception as e:
            print(f"Error: {e}")
 
                    
    def display_users(self):  # method to display users and info COMPLETE
        try: 
            print("Current Users(UserID, Name, LIbraryID):")
            self.library.connect()
            users = self.library.fetch_all("SELECT * FROM users", )
            for user in users:
                print(user)  
            self.library.close() 
         
        except Exception as e:
            print(f"Error: {e}")

