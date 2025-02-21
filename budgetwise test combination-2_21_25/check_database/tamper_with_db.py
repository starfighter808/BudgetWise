import sqlcipher3
import os
import keyring
from pathlib import Path
import sys

app_name = "BudgetWise"
db_filename = "BudgetWise.db"

def get_app_folder():
    """Return the appropriate application data folder for the current OS."""
    if sys.platform.startswith("win"):
        # On Windows, use the APPDATA directory
        base_dir = os.getenv("APPDATA") or os.path.expanduser("~\\AppData\\Roaming")
    elif sys.platform.startswith("darwin"):
        # On macOS, use the Application Support folder
        base_dir = os.path.expanduser("~/Library/Application Support")
    else:
        # For any other OS, default to the user's home directory
        base_dir = os.path.expanduser("~")
    
    app_folder = os.path.join(base_dir, app_name)
    os.makedirs(app_folder, exist_ok=True)  # Create the folder if it doesn't exist
    return app_folder

def edit_db():
    """Allows developers to interact with the encrypted database until they choose to exit."""
    app_data_folder = get_app_folder()
    db_path = Path(app_data_folder) / db_filename

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
