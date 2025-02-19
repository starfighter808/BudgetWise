import sqlcipher3 
import keyring
from pathlib import Path
from installation import Installation
import os

class database():
    def __init__(self, name):
        self.__db_name = f'{name}.db'
        self.__conn = None
        self.__cursor = None

        self.installer = Installation()
        self.app_name = self.installer.app_name
        self.db_filename = self.installer.db_filename

        self.open_db()


    def open_db(self):

        password = keyring.get_password(self.app_name, "db_password")
        if password is None:
            raise Exception("Database password not found. Please run the setup.")

        db_path = os.path.join(self.installer.get_app_folder(), self.db_filename)

        if not os.path.exists(db_path):
            raise Exception(f"Database not found at {db_path}. Please run the setup.")

        try:
            self.conn = sqlcipher3.connect(db_path)
            
            self.conn.execute(f"PRAGMA key='{password}'")

            self.conn.execute("PRAGMA foreign_keys = 1")
            self.cursor = self.conn.cursor()

            print("Database opened successfully.")
        except sqlcipher3.DatabaseError as e:
            print(f"SQLCipher Error: {e}")
            raise

    # debugg funciton                  
    # def print_tables(self):
    #     cursor = self.conn.cursor()  # Create a cursor
    #     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    #     tables = cursor.fetchall()  # Fetch all results

    #     print("we are in the print function")

    #     for table in tables:
    #         print(table[0])  # Print each table name

    def commit_db(self):
        if self.conn:
            self.conn.commit()

    def close_db(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.conn = None
            self.cursor = None

    def check_connection(self):
        
        if self.conn:
            return True
        else:
            return False
