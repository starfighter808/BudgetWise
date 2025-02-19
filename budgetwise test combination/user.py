from Database import database

class User:
    def __init__(self):
        self.db = database()

    def create_user(self, username, password_hash):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO users (username, passwordhash, theme, notificationsEnabled, Language, default_chart) VALUES (?, ?, ?, ?, ?, ?)",
            (username, password_hash, 0, 1, 0, 0)
        )
        self.db.commit_db()

    def get_user_id(self, username):
        cursor = self.db.cursor()
        cursor.execute("SELECT username, passwordhash FROM users WHERE username = ?", (username,))
        return cursor.fetchone()  
