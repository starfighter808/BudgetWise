import os
import platform
import keyring
import keyring.errors
import sqlcipher3
import secrets

class Installation:
    """
    This class is responsible for managing the creation of the encrypted database using sqlcipher3:
    - Detects the operating system to determine where to store the database
    - Creates the necessary directory to store the database
    - Generates a secure password to encrypt the database
    - Creates the database if it does not already exist
    - Retrieves and securely stores the database password
    - Creates the necessary tables in the database

    Attributes:
        db_filename (str): The name of the database file (default: "BudgetWise.db").
        app_folder_name (str): The name of the folder where the database will be stored (default: "BudgetWise").
    """
    def __init__(self, db_filename="BudgetWise.db", app_folder_name="BudgetWise"):
        """
        Initializes the Installation class with the database filename and application folder name.

        Arguments:
            db_filename (str): The name of the database file.
            app_folder_name (str): The folder name where the database will be stored.
        """
        self.db_filename = db_filename  # Set the database file name
        self.app_folder_name = app_folder_name  # Set the folder name where the database will be saved

    def get_app_folder(self):
        """
        Creates a new directory for storing the database if it does not exist, 
        and returns the path to the appropriate application folder based on the operating system.

        Returns:
            str: The directory path to store the database.
        
        Raises:
            ValueError: If the operating system is unsupported.
        """
        os_type = platform.system()  # Check the operating system type

        # Based on the OS type, determine where to store the database
        if os_type == "Windows":
            app_folder = os.path.join(os.getenv("APPDATA"), self.app_folder_name)  # Windows
        elif os_type == "Darwin":
            app_folder = os.path.join(os.path.expanduser("~/Library/Application Support"), self.app_folder_name)  # macOS
        elif os_type == "Linux":
            app_folder = os.path.join(os.path.expanduser("~/.local/share"), self.app_folder_name)  # Linux
        else: 
            raise ValueError(f"Unsupported OS: {os_type}")  # Raise an error if the OS is not supported
        
        # Ensure the application folder exists
        os.makedirs(app_folder, exist_ok=True)
        return app_folder  # Return the folder path

    def generate_random_password(self) -> str:
        """
        Generates a secure 32-byte (256-bit) random password and returns it as a hexadecimal string.

        This password is used to encrypt the database and is stored securely using the `keyring` module.

        Returns:
            str: A 64-character long hexadecimal string representing the generated random password.
        
        Note:
            The default length for `secrets.token_hex()` is 32 bytes (256 bits), providing 
            a high level of randomness suitable for cryptographic use cases.

        References:
            Python documentation for secrets.token_hex: https://docs.python.org/3/library/secrets.html
        """
        return secrets.token_hex(32)  # Generate a secure random password as a hexadecimal string

    def create_encrypted_database(self, db_path=None):
        """
        Creates the encrypted database if it doesn't exist, retrieves the database password,
        and sets up the necessary tables.

        Arguments:
            db_path (str, optional): The file path to the database. If None, the path is derived from the OS.
        
        Raises:
            Exception: If there is an error while creating the database or setting up tables.
        """
        # If no path is provided, generate the path based on the OS
        if db_path is None:
            app_folder = self.get_app_folder()
            db_path = os.path.join(app_folder, self.db_filename)  # Path where the database will be stored
        else:
            os.makedirs(os.path.dirname(db_path), exist_ok=True)  # Ensure the directory for the database exists

        # Retrieve the stored password from the keyring
        password = keyring.get_password(self.app_folder_name, "db_password")
        
        # If no password exists, generate a new one
        if password is None:
            print("Generating a new password for the database...")
            password = self.generate_random_password()  # Generate a new password
            try:
                # Store the generated password securely in the keyring
                keyring.set_password(self.app_folder_name, "db_password", password)
                print("Database password stored securely.")
            except keyring.errors.KeyringError:
                # Handle errors when storing the password in the keyring
                print("Warning: Failed to store the database password securely.")
                print("Save this password manually:", password)
        else:
            print("Using the existing stored password.")  # If a password already exists, use it

        # If the database does not exist, create it
        if not os.path.exists(db_path):
            try:
                # Connect to the database using sqlcipher3
                conn = sqlcipher3.connect(db_path)
                conn.execute(f"PRAGMA key='{password}'")  # Set the encryption key for the database
                conn.execute("PRAGMA foreign_keys = 1")  # Enable foreign key constraints

                # Create the tables in the database
                self.create_tables(conn)
                
                # Commit changes and close the connection
                conn.commit()
                conn.close()
                print(f"Encrypted database created at: {db_path}")
            except Exception as e:
                print("Error creating database:", e)  # Handle any exceptions that occur during database creation
        else:
            print(f"Database already exists at {db_path}")  # Inform the user that the database already exists

    def create_tables(self, conn):
        """
        Creates the necessary tables in the database, if they don't already exist.
        
        Arguments:
            conn (sqlite3.Connection): The database connection object.
        
        Raises:
            Exception: If there is an error while creating the tables.
        """
        cursor = conn.cursor()  # Create a cursor to execute SQL commands

        # SQL script to create the necessary tables
        sql_script = """
        CREATE TABLE IF NOT EXISTS users (
            user_ID INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password_hash TEXT NOT NULL,
            alerts_enabled INTEGER DEFAULT 1,
            default_chart INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            weekly_reports INTEGER DEFAULT 0,
            monthly_reports INTEGER DEFAULT 0,
            yearly_reports INTEGER DEFAULT 0,
            security_question1 TEXT NOT NULL,
            security_question2 TEXT NOT NULL,
            security_question3 TEXT NOT NULL,
            security_question1_answer TEXT NOT NULL,
            security_question2_answer TEXT NOT NULL,
            security_question3_answer TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS budget (
            budgetID INTEGER PRIMARY KEY,
            the_user INTEGER REFERENCES users(userID) ON DELETE CASCADE,
            budget_Name TEXT NOT NULL,
            allocatedMonitaryAmount REAL DEFAULT 0.0,
            start_Date DATETIME NOT NULL,
            end_Date DATETIME NOT NULL
        );

        CREATE TABLE IF NOT EXISTS budget_accounts (
            budget_accounts_id INTEGER PRIMARY KEY,
            the_user INTEGER REFERENCES users(userID) ON DELETE CASCADE,
            the_budget INTEGER REFERENCES budget(budgetID) ON DELETE CASCADE,
            account_name TEXT NOT NULL,
            account_type INTEGER DEFAULT 0,
            balance REAL DEFAULT 0.0,
            savings_goal REAL DEFAULT 0.0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            notes TEXT,
            importance_rating INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS vendor (
            vendor_id INTEGER PRIMARY KEY,
            the_user INTEGER REFERENCES users(userID) ON DELETE CASCADE,
            vendor_name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS alerts (
            alert_id INTEGER PRIMARY KEY,
            budget_accounts_id INTEGER REFERENCES budget_accounts(budget_accounts_id) ON DELETE CASCADE,
            the_user INTEGER REFERENCES users(userID) ON DELETE CASCADE,
            threshhold_amount REAL DEFAULT 0.0,
            alert_type TEXT,
            frequency INTEGER DEFAULT 1,
            status INTEGER DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            active_from DATETIME,
            active_until DATETIME
        );

        CREATE TABLE IF NOT EXISTS report (
            report_id INTEGER PRIMARY KEY,
            the_user INTEGER REFERENCES users(userID) ON DELETE CASCADE,
            report_type INTEGER DEFAULT 0,
            report_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            report_data BLOB
        );

        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY,
            budget_accounts_id INTEGER REFERENCES budget_accounts(budget_accounts_id) ON DELETE CASCADE,
            the_user INTEGER REFERENCES users(userID) ON DELETE CASCADE,
            vendor_id INTEGER REFERENCES vendor(vendor_id) ON DELETE CASCADE,
            transaction_type INTEGER DEFAULT 0,
            amount REAL DEFAULT 0.0,
            transaction_date DATETIME NOT NULL,
            description TEXT,
            recurring INTEGER DEFAULT 0,
            importance_rating INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS audit_log (
            log_id INTEGER PRIMARY KEY,
            the_user INTEGER REFERENCES users(userID) ON DELETE CASCADE,
            transaction_id INTEGER REFERENCES transactions(transaction_id) ON DELETE CASCADE,
            action_type INTEGER DEFAULT 0,
            related_table INTEGER DEFAULT 0,
            record_id INTEGER DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        try:
            # Execute the SQL script to create all tables
            cursor.executescript(sql_script)
            conn.commit()  # Commit the changes to the database
            print("All tables created successfully!")  
        except Exception as e:
            # Handle errors during table creation
            print("Error creating tables:", e)
        finally:
            cursor.close()  # Ensure the cursor is closed after execution
