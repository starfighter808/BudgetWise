import sqlite3

class database():

    def __init__(self, name):
        self.db_name = f'{name}.db'
        self.conn = None
        self.cursor = None
        self.open_db()
        self.create_tables()

    def open_db(self):
        #Open a database connection and create a cursor.
        self.conn = sqlite3.connect(self.db_name)
        self.conn.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.conn.cursor()

    def close_db(self):
        #Commit changes and close the database connection.
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.conn = None
            self.cursor = None

    def create_tables(self):
        # Create users table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
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
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS security_questions (
                    questionID INTEGER PRIMARY KEY,
                    question_text TEXT
                )''')

        # Create user_security_questions table with references to users and security_questions tables
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_security_questions (
                    answer_id INTEGER PRIMARY KEY,
                    the_user INTEGER REFERENCES users(userID),
                    the_question INTEGER REFERENCES security_questions(questionID),
                    answer TEXT
                )''')

        # Create budget table with reference to users table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS budget (
                    budgetID INTEGER PRIMARY KEY,
                    the_user INTEGER REFERENCES users(userID),
                    budget_Name TEXT,
                    allocatedMonitaryAmount REAL,
                    start_Date TEXT,
                    end_Date TEXT
                )''')

        # Create category table with reference to users table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS category (
                    categoryID INTEGER PRIMARY KEY,
                    the_user INTEGER REFERENCES users(userID),
                    catagory_name TEXT,
                    description TEXT,
                    catagory_usage_ranking INTEGER
                )''')

        #   Create budget_accounts table with references to users, category, and budget tables
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS budget_accounts (
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
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS vendor (
                    vendor_id INTEGER PRIMARY KEY,
                    the_user INTEGER REFERENCES users(userID),
                    vendor_name TEXT,
                    description TEXT,
                    vendor_usage_ranking INTEGER
                )''')

        # Create alerts table with references to budget_accounts and users tables
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS alerts (
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
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS report (
                    report_id INTEGER PRIMARY KEY,
                    the_user INTEGER REFERENCES users(userID),
                    report_type INTEGER,
                    report_date TEXT,
                    report_data BLOB,
                    report_frequency INTEGER
                )''')
   
        # Create transactions table with references to budget_accounts, users, category, and vendor tables
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
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
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS audit_log (
                    log_id INTEGER PRIMARY KEY,
                    the_user INTEGER REFERENCES users(userID),
                    transaction_id INTEGER REFERENCES transactions(transaction_id),
                    action_type INTEGER,
                    related_table INTEGER,
                    record_id INTEGER,
                    timestamp TEXT
                )''')