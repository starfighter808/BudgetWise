import platform
import subprocess
import shutil
import urllib.request
import os
import keyring
import keyring.errors
import sqlcipher3
import secrets
import string
import importlib
import sys
from pathlib import Path

class Installation:

    def __init__(self):
        self.app_name = "BudgetWise"
        self.db_filename = "BudgetWise.db"
        self.os_type = self.check_os()

    """ 
        Check OS is to figure out the operating to system that the code is running on. This is important as it will decide how the rest of the code operates.
        This funciton relies on using the platform library using the system funciton in it to get the os name.
        Then using an if block we deteremine if it is mac os, windows or unsupported os.
    """
    def check_os(self) -> str:
        check_os = platform.system()
        if check_os == 'Darwin':
            return "MacOS"
        elif check_os == 'Windows':
            return "Windows"
        else:
            raise OSError("Unsupported OS. This script currently supports Windows and MacOS only.")

    """ 
        get_app_folder funciton is used to figure out where the database is going to be stored/which os/what the file path is to be used.
        It uses an if block to return the corect file path type for the other functions to use later on.
    """
    def get_app_folder(self):
        if self.os_type == "Windows":
            return os.path.join(os.getenv("APPDATA"), self.app_name)
        elif self.os_type == "MacOS":
            return os.path.join(os.path.expanduser("~/Library/Application Support"), self.app_name)
        else:
            raise OSError("Unsupported OS")

    """
        check_python works to determine if python is installed by checking for either python or python3. 
        If python is not found it will call the download and install python funciton.
        Once it either installs python or finds it will determine the version that is installed. 
        Ideally we then compare the version if it is per installed to know if it will work if it wont then call download and install python to get a good version.
    """
    def check_python(self) -> str: 
        python_exe = shutil.which("python") or shutil.which("python3")
        
        if not python_exe:
            if  not self.download_and_install_python():
                return "python failed to install"
        
        try:
            result = subprocess.run(
                [python_exe, "--version"],
                capture_output=True, 
                text=True,
                check=True
            )
            python_version = result.stdout.strip() or result.stderr.strip()
            print(f"Python is installed: {python_version}")
            return python_version
        except subprocess.CalledProcessError:
            print("Error occurred while trying to retrieve Python version.")
            return "python failed to install"

    def download_and_install_python(self) -> bool:
        if self.os_type == "Windows":
            python_installer_url = "https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe"
            installer_path = "python-installer.exe"
        elif self.os_type == "MacOS":
            python_installer_url = "https://www.python.org/ftp/python/3.13.1/python-3.13.1-macos11.pkg"
            installer_path = "python-installer.pkg"
        else:
            return False

        print(f"Downloading Python installer for {self.os_type} from {python_installer_url}...")

        try:
            urllib.request.urlretrieve(python_installer_url, installer_path)
            print(f"Download completed: {installer_path}")

            # Run the installer
            if self.os_type == "Windows":
                try:
                    subprocess.run([installer_path, "/quiet", "InstallAllUsers=1", "PrependPath=1"], check=True)
                    print("Python installation completed for Windows!")
                except subprocess.CalledProcessError as e:
                    print(f"Error occurred during Windows installation: {e}")
                    return False
            elif self.os_type == "MacOS":
                try:
                    subprocess.run(["sudo", "installer", "-pkg", installer_path, "-target", "/"], check=True)
                    print("Python installation completed for macOS!")
                except subprocess.CalledProcessError as e:
                    print(f"Error occurred during macOS installation: {e}")
                    return False
        except Exception as e:
            print(f"Failed to download or install Python: {e}")
            return False
        finally:
            if os.path.exists(installer_path):
                os.remove(installer_path)

        # Double-check if Python is installed after running the installer
        python_exe = shutil.which("python") or shutil.which("python3")
        if not python_exe:
            print("Python installation failed. Please manually install Python.")
            return False

        return True



    def generate_random_password(self,length=32) -> str:
        """Generate a random password with letters, digits, and special characters."""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(characters) for _ in range(length))
    
    def check_library_status(self) -> bool:
        required_libraries = {
            "Windows": {"sqlcipher3": "sqlcipher3-wheels", "keyring": "keyring"},
            "MacOS": {"sqlcipher3": "sqlcipher3", "keyring": "keyring"}
        }

        os_libs = required_libraries.get(self.os_type, {})

        # Check for missing libraries
        missing_libraries = [lib for lib in os_libs if not self.is_library_installed(lib)]

        if missing_libraries:
            print(f"Installing missing libraries: {', '.join(missing_libraries)}...")
            if not self.install_libraries([os_libs[lib] for lib in missing_libraries]):
                print("Failed to install required libraries.")
                return False

        return True

    def is_library_installed(self, library_name: str) -> bool:
        """Check if a library is installed."""
        try:
            importlib.import_module(library_name)
            return True
        except ImportError:
            return False

    def install_libraries(self, libraries: list) -> bool:
        """Install a list of libraries using pip."""
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *libraries])
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error installing libraries: {e}")
            return False  # Ensure failure is returned



    def create_encrypted_database(self):
        """Creates an encrypted database and initializes tables."""
        app_data_folder = self.get_app_folder()
        Path(app_data_folder).mkdir(parents=True, exist_ok=True)

        db_path = Path(app_data_folder) / self.db_filename

        # Retrieve or generate a secure password
        password = keyring.get_password(self.app_name, "db_password")
        if password is None:
            print("Generating a new password for the database...")
            password = self.generate_random_password()
            try:
                keyring.set_password(self.app_name, "db_password", password)
                print("Database password securely stored.")
            except keyring.errors.KeyringError:
                print("Warning: Failed to store the database password securely.")
                print("Ensure you save this password manually: ", password)
        else:
            print("Using the existing stored password.")

        # Create the database if it does not exist
        if not os.path.exists(db_path):
            try:
                conn = sqlcipher3.connect(db_path)
                conn.execute(f"PRAGMA key='{password}'")
                conn.execute("PRAGMA foreign_keys = 1")
                cursor = conn.cursor()

                self.create_tables(cursor)

                conn.commit()
                conn.close()
                print(f"Encrypted database created at: {db_path}")

            except Exception as e:
                print(f"Error creating database: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"Database already exist at {db_path}")

    def create_tables(self, cursor):
        tables = [
            '''CREATE TABLE IF NOT EXISTS users (
                userID INTEGER PRIMARY KEY,
                username TEXT,
                passwordhash TEXT,
                theme INTEGER,
                notificationsEnabled INTEGER,
                Language INTEGER,
                default_chart INTEGER,
                createdAt TEXT,
                updatedAT TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS security_questions (
                questionID INTEGER PRIMARY KEY,
                question_text TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS user_security_questions (
                the_user INTEGER PRIMARY KEY REFERENCES users(userID),
                the_question INTEGER REFERENCES security_questions(questionID),
                answer TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS budget (
                budgetID INTEGER PRIMARY KEY,
                the_user INTEGER REFERENCES users(userID),
                budget_Name TEXT,
                allocatedMonitaryAmount REAL,
                start_Date TEXT,
                end_Date TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS category (
                categoryID INTEGER PRIMARY KEY,
                the_user INTEGER REFERENCES users(userID),
                category_name TEXT,
                description TEXT,
                category_usage_ranking INTEGER
            )''',
            '''CREATE TABLE IF NOT EXISTS budget_accounts (
                budget_accounts_id INTEGER PRIMARY KEY,
                the_user INTEGER REFERENCES users(userID),
                the_category INTEGER REFERENCES category(categoryID),
                the_budget INTEGER REFERENCES budget(budgetID),
                account_name TEXT,
                account_type INTEGER,
                balance REAL,
                savings_goal REAL,
                created_at TEXT,
                updated_at TEXT,
                notes TEXT,
                importance_rating INTEGER
            )''',
            '''CREATE TABLE IF NOT EXISTS vendor (
                vendor_id INTEGER PRIMARY KEY,
                the_user INTEGER REFERENCES users(userID),
                vendor_name TEXT,
                description TEXT,
                vendor_usage_ranking INTEGER
            )''',
            '''CREATE TABLE IF NOT EXISTS alerts (
                alert_id INTEGER PRIMARY KEY,
                budget_accounts_id INTEGER REFERENCES budget_accounts(budget_accounts_id),
                the_user INTEGER REFERENCES users(userID),
                threshold_amount REAL,
                alert_type TEXT,
                frequency INTEGER,
                status INTEGER,
                created_at TEXT,
                updated_at TEXT,
                active_from TEXT,
                active_until TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY,
                budget_accounts_id INTEGER REFERENCES budget_accounts(budget_accounts_id),
                the_user INTEGER REFERENCES users(userID),
                the_category INTEGER REFERENCES category(categoryID),
                vendor_id INTEGER REFERENCES vendor(vendor_id),
                transaction_type INTEGER,
                amount REAL,
                transaction_date TEXT,
                description TEXT,
                recurring INTEGER,
                importance_rating INTEGER
            )'''
        ]

        for table in tables:
            cursor.execute(table)


    def edit_db(self):
        """Allows the user to interact with the encrypted database until they choose to exit."""
        app_data_folder = self.get_app_folder()
        db_path = Path(app_data_folder) / self.db_filename

        # Retrieve the database password from keyring
        password = keyring.get_password(self.app_name, "db_password")
        if password is None:
            print("Error: No password found for database. Cannot proceed.")
            return

        try:
            conn = sqlcipher3.connect(db_path)
            conn.execute(f"PRAGMA key='{password}'")
            conn.execute("PRAGMA foreign_keys = 1") 
            cursor = conn.cursor()

            print("Connected to the database. Type SQL commands or 'exit' to finish.")

            while True:
                user_input = input("SQL> ").strip()

                if user_input.lower() in {"exit", "quit", ".q"}:
                    while True:
                        commit_or_not = input("Would you like to commit changes? (yes/no): ").strip().lower()
                        if commit_or_not in {"yes", "y"}:
                            print("Committing changes and closing database connection.")
                            conn.commit()
                            break
                        elif commit_or_not in {"no", "n"}:
                            print("Closing database connection without saving changes.")
                            break
                        else:
                            print("Invalid input. Please enter 'yes' or 'no'.")
                    break

                try:
                    cursor.execute(user_input)
                    if user_input.lower().startswith("select"):
                        print(cursor.fetchall())  
                    else:
                        print("Query executed successfully.")
                except Exception as e:
                    print(f"Error executing SQL: {e}")

            conn.close()
        except Exception as e:
            print(f"Error connecting to the database: {e}")
