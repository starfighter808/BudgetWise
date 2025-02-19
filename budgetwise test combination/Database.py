import sqlcipher3
import keyring
import os
import threading
from installation import Installation

class database:
    _instance = None  
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(database, cls).__new__(cls)
                cls._instance.__conn = None
                cls._instance.__cursor = None
                cls._instance.installer = Installation()
                cls._instance.db_filename = "BudgetWise.db"
                cls._instance.open_db()
            return cls._instance

    def open_db(self):
        db_path = os.path.join(self.installer.get_app_folder(), self.db_filename)

        if not os.path.exists(db_path):
            raise FileNotFoundError(f"database not found at {db_path}. Please run the setup.")

        password = keyring.get_password(self.installer.app_name, "db_password")
        if password is None:
            raise Exception("database password not found. Please run the setup.")

        try:
            if self.__conn is None:
                self.__conn = sqlcipher3.connect(db_path, check_same_thread=False)
                self.__conn.execute(f"PRAGMA key='{password}'")
                self.__conn.execute("PRAGMA foreign_keys = 1")
                self.__cursor = self.__conn.cursor()
                print("database opened successfully.")
            else:
                print("database connection already established.")
        except sqlcipher3.databaseError as e:
            print(f"SQLCipher Error: {e}")
            raise

    def cursor(self):
        if self.__cursor is None:
            raise Exception("Cursor is not initialized. Ensure the database connection is opened first.")
        return self.__cursor

    def commit_db(self):
        if self.__conn:
            self.__conn.commit()

    def close_db(self):
        with self._lock:
            if self.__conn:
                self.__conn.commit()
                self.__conn.close()
                self.__conn = None
                self.__cursor = None
                print("database connection closed.")

    def check_connection(self):
        return self.__conn is not None
