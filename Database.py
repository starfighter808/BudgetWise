import sqlite3

# Create a connection to the database (creates the database if it doesn't exist)
conn = sqlite3.connect('Budgetwise.db')


conn.execute("PRAGMA foreign_keys = 1")

# Create a cursor object
cursor = conn.cursor()

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    userID INTEGER PRIMARY KEY,
                    username TEXT,
                    passwordhash Text,
                    theme INTEGER,
                    notificationsEnabled INTEGER,
                    Language TEXT,
                    createdAt TEXT,
                    updatedAT TEXT
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS security_questions (
                    questionID INTEGER PRIMARY KEY,
                    question_text TEXT
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS user_security_questions (
                    the_user INTEGER PRIMARY KEY REFERENCES users(userID),
                    the_question INTEGER REFERENCES security_questions(questionID),
                    answer TEXT
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS budget (
                    budgetID INTEGER PRIMARY KEY,
                    the_user INTEGER REFERENCES users(userID),
                    budget_Name TEXT,
                    allocatedMonitaryAmount INTEGER,
                    start_Date TEXT,
                    end_Date TEXT
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS category (
                    categoryID INTEGER PRIMARY KEY,
                    the_user INTEGER REFERENCES users(userID),
                    catagory_name TEXT,
                    description TEXT,
                    catagory_usage_ranking INTEGER
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS budget_accounts (
                    budget_accounts_id INTEGER PRIMARY KEY,
                    the_user INTEGER REFERENCES users(userID),
                    the_category INTEGER REFERENCES category(categoryID),
                    the_budget INTEGER REFERENCES budget(budgetID),
                    account_name TEXT,
                    account_type TEXT,
                    balance INTEGER,
                    savings_goal INTEGER,
                    created_at TEXT,
                    updated_at TEXT,
                    notes TEXT,
                    importamce_rating INTEGER
                )''')



# Commit the changes
conn.commit()

# Close the connection
conn.close()