# module for databse class to connect to and manipulate
import mysql.connector


class Database:  # Database class, initializes information to access database    
    def __init__(self, host, database, password, user):
        self.host = host
        self.database = database
        self.password = password
        self.user = user
        self.host = host
         
        
    def connect(self):  # method to connect to database
        try:
            self.connection = mysql.connector.connect(
                database = self.database, 
                password = self.password,
                host = self.host, 
                user = self.user 
            ) 
            self.cursor = self.connection.cursor()             
        except Exception as e:
            print(f"Error: {e}") 
        
    
    def close(self):   # method to close connection
        try:
            if self.connection:
                self.connection.close() 
                self.cursor.close() 
        except Exception as e:
            print(f"Error: {e}")
    
    
    def execute_query(self, query, params=None):   # method to execute query 
        try:   
            self.cursor.execute(query, params) 
            self.connection.commit() 
        except Exception as e:
            print(f"Error: {e}")   
           
    def fetch_all(self, query):   # method to fetch data, query entered in call 
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            print(f"Error: {e}")
            return None
    
