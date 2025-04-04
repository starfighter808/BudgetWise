import os
import keyring
from pathlib import Path
import sys
import platform
import sqlcipher3


app_name = "BudgetWise"
db_filename = "BudgetWise.db"

def get_app_folder():
    """Return the proper application folder depending on the OS and create it if needed."""
        
    os_type = platform.system() 

    if os_type == "Windows":
        app_folder = os.path.join(os.getenv("APPDATA"), app_name)  
    elif os_type == "Darwin":  
        app_folder = os.path.join(os.path.expanduser("~/Library/Application Support"), app_name)  
    elif os_type == "Linux":  
        app_folder = os.path.join(os.path.expanduser("~/.local/share"), app_name) 
        print(app_folder)
    else:
        raise ValueError(f"Unsupported OS: {os_type}")

    os.makedirs(app_folder, exist_ok=True) 
    return app_folder

def edit_db():
    """Allows developers to interact with the encrypted database until they choose to exit."""
    app_folder = get_app_folder()
    Path(app_folder).mkdir(parents=True, exist_ok=True)
    db_path = os.path.join(app_folder, db_filename)

    # Retrieve the database password from keyring
    password = keyring.get_password(app_name, "db_password")
    if password is None:
        print("Error: No password found for the database. Cannot proceed.")
        return

    try:
        conn = sqlcipher3.connect(db_path)
        # Be cautious: if the password contains special characters like a single quote,
        # you might need additional handling or escaping.
        conn.execute(f"PRAGMA key='{password}'")
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()

        print("Connected to the database. Type SQL commands or 'exit' to finish.")

        # List existing tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            print(table[0])  # Print each table name

        # Interactive SQL prompt
        while True:
            user_input = input("SQL> ").strip()
            if user_input.lower() in {"exit", "quit", ".q"}:
                while True:
                    commit_or_not = input("Would you like to commit changes? (yes/no): ").strip().lower()
                    if commit_or_not in {"yes", "y"}:
                        print("Committing changes and closing the database connection.")
                        conn.commit()
                        break
                    elif commit_or_not in {"no", "n"}:
                        print("Closing the database connection without saving changes.")
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

def main():
    edit_db()

if __name__ == "__main__":
    sys.exit(main())
