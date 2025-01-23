import os
import keyring
import sqlcipher3
import secrets
import string

# Check if library's are installed
def check_library_status() -> bool:
    flag1 = False
    flag2 = False
    flag3 = False
    flag4 = False
    flag5 = False 

    all_clear = False

    # Checking for sqlcipher
    try:
        import sqlcipher3
        print("sqlcipher3 is installed")
        flag1 = True
    except ImportError:
        print("sqlcipher3 is not installed")

    # Checking for keyring
    try:
        import keyring
        print("keyring is installed")
        flag2 = True
    except ImportError:
        print("keyring is not installed")

    # Checking for os
    try:
        import os
        print("os is available")
        flag3 = True
    except ImportError:
        print("os is not installed")
    
    # Checking for secrets
    try:
        import secrets
        print("secrets is available")
        flag4 = True
    except ImportError:
        print("secrets is not installed")

    # Checking for string
    try:
        import string
        print("string is available")
        flag5 = True
    except ImportError:
        print("string is not installed")

    # Checking to see if all are true
    if(flag1 and flag2 and flag3 and flag4 and flag5):
        all_clear = True
    
    return (all_clear)

def generate_random_password(length=32) -> str:
    """Generate a random password with letters, digits, and special characters."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return (password)


def create_encrypted_database():
    # Get the path to the Application Support folder
    app_support_folder = os.path.expanduser('~/Library/Application Support')
    app_name = 'BudgetWise'  # Folder name 
    app_folder = os.path.join(app_support_folder, app_name)

    # Create the folder if it does not exist
    if not os.path.exists(app_folder):
        os.makedirs(app_folder)
        print(f"Created folder at: {app_folder}")

    # Define the full path for the database
    db_path = os.path.join(app_folder, 'BudgetWise.db')

    # Check if password already exists in keyring
    password = keyring.get_password('BudgetWise', 'db_password')
    if password is None:
        password = generate_random_password()
        keyring.set_password('BudgetWise', 'db_password', password)
        print("Password has been securely stored in the macOS Keychain.")

    # Create the database if it does not exist
    if not os.path.exists(db_path):
        conn = sqlcipher3.connect(db_path)
        conn.execute(f"PRAGMA key='{password}'") 
        print(f"Encrypted database created at: {db_path}")
        conn.close()

    # Connect to the database
    conn = sqlcipher3.connect(db_path)
    conn.execute(f"PRAGMA key='{password}'") 
    conn.execute(f"ATTACH DATABASE '{db_path}' AS encrypted KEY '{password}';")

    # Enable foreign key constraint
    conn.execute("PRAGMA foreign_keys = 1")

    # Create a cursor object
    cursor = conn.cursor()

     Create users table
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    userID INTEGER PRIMARY KEY,
                    username TEXT,
                    passwordhash TEXT,
                    theme INTEGER,
                    notificationsEnabled INTEGER,
                    Language INTEGER,
                    default_chart INTEGER,
                    createdAt TEXT,
                    updatedAT TEXT
                )''')

# Create security_questions table
cursor.execute('''CREATE TABLE IF NOT EXISTS security_questions (
                    questionID INTEGER PRIMARY KEY,
                    question_text TEXT
                )''')

# Create user_security_questions table with references to users and security_questions tables
cursor.execute('''CREATE TABLE IF NOT EXISTS user_security_questions (
                    the_user INTEGER PRIMARY KEY REFERENCES users(userID),
                    the_question INTEGER REFERENCES security_questions(questionID),
                    answer TEXT
                )''')

# Create budget table with reference to users table
cursor.execute('''CREATE TABLE IF NOT EXISTS budget (
                    budgetID INTEGER PRIMARY KEY,
                    the_user INTEGER REFERENCES users(userID),
                    budget_Name TEXT,
                    allocatedMonitaryAmount REAL,
                    start_Date TEXT,
                    end_Date TEXT
                )''')

# Create category table with reference to users table
cursor.execute('''CREATE TABLE IF NOT EXISTS category (
                    categoryID INTEGER PRIMARY KEY,
                    the_user INTEGER REFERENCES users(userID),
                    catagory_name TEXT,
                    description TEXT,
                    catagory_usage_ranking INTEGER
                )''')

# Create budget_accounts table with references to users, category, and budget tables
cursor.execute('''CREATE TABLE IF NOT EXISTS budget_accounts (
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
                )''')

# Create vendor table with reference to users table
cursor.execute('''CREATE TABLE IF NOT EXISTS vendor (
                    vendor_id INTEGER PRIMARY KEY,
                    the_user INTEGER REFERENCES users(userID),
                    vendor_name TEXT,
                    description TEXT,
                    vendor_usage_ranking INTEGER
                )''')

# Create alerts table with references to budget_accounts and users tables
cursor.execute('''CREATE TABLE IF NOT EXISTS alerts (
                    alert_id INTEGER PRIMARY KEY,
                    budget_accounts_id INTEGER REFERENCES budget_accounts(budget_accounts_id),
                    the_user INTEGER REFERENCES users(userID),
                    threshhold_amount REAL,
                    alert_type TEXT,
                    frequency INTEGER,
                    status INTEGER,
                    created_at TEXT,
                    updated_at TEXT,
                    active_from TEXT,
                    actice_until TEXT
                )''')

# Create report table with reference to users table
cursor.execute('''CREATE TABLE IF NOT EXISTS report (
                    report_id INTEGER PRIMARY KEY,
                    the_user INTEGER REFERENCES users(userID),
                    report_type INTEGER,
                    report_date TEXT,
                    report_data BLOB,
                    report_frequency INTEGER
                )''')
   
# Create transactions table with references to budget_accounts, users, category, and vendor tables
cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
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
                )''')

# Create audit_log table with references to users and transactions tables
cursor.execute('''CREATE TABLE IF NOT EXISTS audit_log (
                    log_id INTEGER PRIMARY KEY,
                    the_user INTEGER REFERENCES users(userID),
                    transaction_id INTEGER REFERENCES transactions(transaction_id),
                    action_type INTEGER,
                    related_table INTEGER,
                    record_id INTEGER,
                    timestamp TEXT
                )''')
    
    conn.execute('CREATE TABLE IF NOT EXISTS testUsers (test_id INTEGER PRIMARY KEY, test_name TEXT);')
    conn.execute('INSERT INTO testUsers (test_name) VALUES ("Alice"), ("Bob");')


    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print(f"Encrypted database created and tables set up at: {db_path}")


def decrypt_database():
    # Get the path to the Application Support folder
    app_support_folder = os.path.expanduser('~/Library/Application Support')
    app_name = 'BudgetWise'  
    app_folder = os.path.join(app_support_folder, app_name)

    db_path = os.path.join(app_folder, 'BudgetWise.db')

    # Retrieve the password from Keychain
    password = keyring.get_password('BudgetWise', 'db_password')
    if password is None:
                
        return(print("No password found in Keychain. Please create the database first."))

    # Connect to the encrypted database and retrieve password
    conn = sqlcipher3.connect(db_path)
    conn.execute(f"PRAGMA key='{password}'") 
    conn.execute(f"ATTACH DATABASE '{db_path}' AS encrypted KEY '{password}'")

    # Create a cursor object
    cursor = conn.cursor()

    # Example: Query users table to verify access
    cursor.execute("SELECT * FROM testUsers")
    rows = cursor.fetchall()

    # Print the result of the query
    print("Retrieved data from 'testUsers' table:")
    for row in rows:
        print(row)

    # Close the connection
    conn.close()


def main():
    library_status = check_library_status()

    if library_status:
        print("All libraries are properly installed!")
        #create_encrypted_database()

        decrypt_database()
    else:
        print("There is one or more missing libraries :(")


if __name__ == "__main__":
    main()
