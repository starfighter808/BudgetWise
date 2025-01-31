# TODO:
# * Normalize all variable names in database.py for consistency
# * createdAt and updatedAT should be timestamps. This can be done with 'createdAt TEXT DEFAULT (datetime('now', 'localtime'))

from database import Database

class User:
    def __init__(self, conn: Database):
        self.conn = conn

    def create_user(self, username, password_hash):
        query = "INSERT INTO users (username, passwordhash, theme, notificationsEnabled, Language, default_chart) VALUES (?, ?, ?, ?, ?, ?)"
        self.conn.execute(query, (username, password_hash, 0, 1, 0, 0))

    def get_user_id(self, username, password_hash):
        query = "SELECT * FROM users WHERE username = ? AND passwordhash = ?"
        return self.conn.fetchone(query, (username, password_hash))
    

