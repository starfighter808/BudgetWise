import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.Connection("budgetwise_db")
        self.cursor = self.connection.cursor()
        self.create_tables()

    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetchone(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
    
    def fetchall(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def create_tables(self):
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
        

    
    def close(self):
        self.connection.close()