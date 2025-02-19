import Database

class User:
    def __init__(self, conn: Database):
        self.conn = conn  # This is actually the 'database' object, not an SQLite3 connection
        self.cursor = self.conn.cursor  # Use the cursor object directly

    def create_user(self, username, password_hash):
        query = "INSERT INTO users (username, passwordhash, theme, notificationsEnabled, Language, default_chart) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.execute(query, (username, password_hash, 0, 1, 0, 0))
        self.conn.commit_db()  # Commit the changes using commit_db()

    def get_user_id(self, username):
        query = "SELECT username, passwordhash FROM users WHERE username = ?"
        self.cursor.execute(query, (username,))
        return self.cursor.fetchone()  

