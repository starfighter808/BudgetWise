import os
import platform
import keyring
import keyring.errors
import sqlcipher3
import secrets
from pathlib import Path

class Installation:
    def __init__(self, db_filename="BudgetWise.db", app_name="BudgetWise"):
        self.db_filename = db_filename
        self.app_name = app_name
        self.os_type = platform.system() 
    
    def get_app_folder(self):
        """Return the proper application folder depending on the OS."""
        if self.os_type == "Windows":
            return os.path.join(os.getenv("APPDATA"), self.app_name)
        elif self.os_type == "Darwin":
            return os.path.join(os.path.expanduser("~/Library/Application Support"), self.app_name)
        else:
            # For Linux potentially, work in progress
            #return os.path.join(os.path.expanduser("~"), f".{self.app_name}")
            print("invalid os")

    def generate_random_password(self, length=32) -> str:
        """Generate a secure random password."""
        return secrets.token_hex(length)

    def create_encrypted_database(self):
        """Create the encrypted database (if it doesn't exist) and store/retrieve the key."""
        app_folder = self.get_app_folder()
        Path(app_folder).mkdir(parents=True, exist_ok=True)
        db_path = os.path.join(app_folder, self.db_filename)

        password = keyring.get_password(self.app_name, "db_password")
        if password is None:
            print("Generating a new password for the database...")
            password = self.generate_random_password(32)
            try:
                keyring.set_password(self.app_name, "db_password", password)
                print("Database password stored securely.")
            except keyring.errors.KeyringError:
                print("Warning: Failed to store the database password securely.")
                print("Save this password manually:", password)
        else:
            print("Using the existing stored password.")

        if not os.path.exists(db_path):
            try:
                conn = sqlcipher3.connect(db_path)
                conn.execute(f"PRAGMA key='{password}'")
                conn.execute("PRAGMA foreign_keys = 1")

                self.create_tables(conn)
                
                conn.commit()
                conn.close()
                print(f"Encrypted database created at: {db_path}")
            except Exception as e:
                print("Error creating database:", e)
        else:
            print(f"Database already exists at {db_path}")

    def create_tables(self, conn):
        
        cursor = conn.cursor()
        sql_script = """
        CREATE TABLE IF NOT EXISTS users (
            userID INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            passwordhash TEXT NOT NULL,
            theme INTEGER DEFAULT 0,
            notificationsEnabled INTEGER DEFAULT 1,
            Language INTEGER DEFAULT 0,
            default_chart INTEGER DEFAULT 0,
            createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
            updatedAT DATETIME DEFAULT CURRENT_TIMESTAMP,
            weekly_reports INTEGER DEFAULT 0,
            monthly_reports INTEGER DEFAULT 0,
            yearly_reports INTEGER DEFAULT 0,
            security_question BLOB
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
            cursor.executescript(sql_script)
            conn.commit()
            print("All tables created successfully!")
        except Exception as e:
            print("Error creating tables:", e)
        finally:
            cursor.close()
