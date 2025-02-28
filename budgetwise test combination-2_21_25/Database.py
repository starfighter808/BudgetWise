import sqlcipher3
import keyring
import threading
from pathlib import Path

class Database:
    """
    This class handles the connection to a SQLCipher-encrypted database, ensuring a single instance 
    of the connection (Singleton pattern). It is responsible for:
    - Opening the database connection.
    - Ensuring the database is properly unlocked using the stored password.
    - Providing access to a database cursor for querying.
    - Committing changes to the database and closing the connection.
    
    Attributes:
        _instance (Database, optional): A singleton instance of the Database class.
        _lock (threading.Lock): A lock to prevent race conditions while accessing the singleton instance.
        installer (Installation): An instance of the Installation class to get app-specific details like the database path.
        db_filename (str): The filename of the database to connect to (default is "BudgetWise.db").
        __conn (sqlcipher3.Connection, optional): The database connection object.
        __cursor (sqlcipher3.Cursor, optional): The database cursor used for querying.
        _initialized (bool): Flag indicating whether the class has been initialized.
    """
    _instance = None  # Singleton instance
    _lock = threading.Lock()  # Lock to synchronize access to the singleton instance

    def __init__(self, installer, db_filename="BudgetWise.db"):
        """
        Initializes the Database class. This method is part of the Singleton pattern and prevents 
        multiple instances from being created.

        Arguments:
            installer (Installation): The installer object responsible for app-related configurations.
            db_filename (str): The name of the database file to connect to (default: "BudgetWise.db").
        """
        # Prevent reinitialization if the instance has already been initialized
        if hasattr(self, '_initialized') and self._initialized:
            return

        self.installer = installer  # Store the installer object
        self.db_filename = db_filename  # Store the database filename
        self.__conn = None  # Initialize the connection attribute as None
        self.__cursor = None  # Initialize the cursor attribute as None
        self._initialized = True  # Mark the class as initialized
        self.open_db()  # Open the database connection during initialization

    @classmethod
    def get_instance(cls, installer, db_filename="BudgetWise.db"):
        """
        Returns the Singleton instance of the Database class. If the instance doesn't exist, 
        it creates one and opens the database connection.

        Arguments:
            installer (Installation): The installer object responsible for app-related configurations.
            db_filename (str): The name of the database file to connect to (default: "BudgetWise.db").
        
        Returns:
            Database: The singleton instance of the Database class.
        """
        with cls._lock:  # Ensure thread-safety when accessing the singleton instance
            if cls._instance is None:
                # If no instance exists, create a new one
                cls._instance = cls(installer, db_filename)
            return cls._instance  # Return the singleton instance
    
    def open_db(self):
        """
        Opens a connection to the encrypted database. If the connection is already open, it returns early.

        This method:
        - Checks if the database exists at the expected path.
        - Retrieves the database password from the keyring.
        - Initializes the SQLCipher connection with the password and opens a cursor.
        
        Raises:
            FileNotFoundError: If the database file does not exist.
            Exception: If the database password is not found in the keyring.
            sqlcipher3.DatabaseError: If there is a database error when opening the connection.
        """
        if self.__conn is not None:
            print("Database connection already established.")
            return  # Prevent reopening the connection if it's already open
        
        # Build the database path using Pathlib for platform-independent path handling
        app_folder = Path(self.installer.get_app_folder())  # Get the app's folder path
        db_path = app_folder / self.db_filename  # Construct the full database file path

        # Check if the database file exists at the specified path
        if not db_path.exists():
            raise FileNotFoundError(f"Database not found at {db_path}. Please run the setup.")

        # Retrieve the stored database password from the keyring
        password = keyring.get_password(self.installer.app_folder_name, "db_password")
        if password is None:
            raise Exception("Database password not found. Please run the setup.")

        try:
            # Attempt to establish a connection to the database using SQLCipher
            self.__conn = sqlcipher3.connect(str(db_path), check_same_thread=False)
            self.__conn.execute(f"PRAGMA key='{password}'")  # Set the encryption key for SQLCipher
            self.__conn.execute("PRAGMA foreign_keys = 1")  # Enable foreign key support
            self.__cursor = self.__conn.cursor()  # Initialize the cursor for database queries
            print("Database opened successfully.")
        except sqlcipher3.DatabaseError as e:
            # Handle any errors that occur when opening the database
            print(f"SQLCipher Error: {e}")
            raise

    def cursor(self):
        """
        Returns the database cursor for querying the database.

        Returns:
            sqlcipher3.Cursor: The database cursor.

        Raises:
            Exception: If the cursor is not initialized (i.e., the database connection was not opened).
        """
        if self.__cursor is None:
            raise Exception("Cursor is not initialized. Ensure the Database connection is opened first.")
        return self.__cursor  # Return the cursor for executing queries

    def commit_db(self):
        """
        Commits any changes made to the database using the current connection.

        This method is used to save changes (e.g., inserts, updates, deletes) to the database.

        Raises:
            Exception: If the database connection is not open.
        """
        if self.__conn:
            self.__conn.commit()  # Commit changes to the database
        else:
            raise Exception("Database connection not established. Cannot commit changes.")

    def close_db(self):
        """
        Closes the database connection and cursor, cleaning up resources.

        This method ensures that the connection is properly closed and the cursor is discarded.

        Uses a lock to prevent race conditions when closing the connection.
        """
        with self._lock:  # Ensure thread-safety when closing the connection
            if self.__conn is not None:
                # Commit any outstanding changes before closing the connection
                self.__conn.commit()
                self.__conn.close()  # Close the connection
                self.__conn = None  # Reset the connection attribute
                self.__cursor = None  # Reset the cursor attribute
                print("Database connection closed.")
            else:
                print("Database connection already closed.")  # Inform if the connection was already closed

    def check_connection(self):
        """
        Checks if the database connection is currently open.

        Returns:
            bool: True if the database connection is open, otherwise False.
        """
        return self.__conn is not None  # Return True if the connection is open, otherwise False
