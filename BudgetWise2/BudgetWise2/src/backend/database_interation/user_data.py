from argon2 import PasswordHasher
import sqlcipher3

class UserData:
    """
    Handles user-related database operations:
    - Fetching user details
    - Retrieving and validating security questions & answers
    - Updating passwords securely
    """

    def __init__(self, db_instance):
        """Initialize with database instance and Argon2 password hasher."""
        self.db = db_instance
        self.ph = PasswordHasher()
        self.temp_info = {}
        self.temp_questions = {}
        self.temp_answers = {}

    def get_user_by_username(self, username):
        """Fetch user details by username (excluding sensitive data)."""
        username = username.strip() if isinstance(username, str) else None
        if not username:
            return None

        try:
            cursor = self.db.cursor()
            cursor.execute(
                """SELECT username FROM users WHERE username = ?""",
                (username,)
            )
            result = cursor.fetchone()
            print(f"Fetched user result: {result}")
        except sqlcipher3.Error as e:
            print(f"Database error while fetching user: {e}")
            result = None

        return result  

    def get_security_questions(self, username):
        """
        Retrieve security questions and their corresponding answers.
        Returns a dictionary with keys 'questions' and 'answers' if found,
        or None if no record is found.
        """
        username = username.strip() if isinstance(username, str) else None
        if not username:
            return None

        try:
            cursor = self.db.cursor()
            cursor.execute(
                """SELECT security_question1, security_question2, security_question3, 
                          security_question1_answer, security_question2_answer, security_question3_answer
                   FROM users WHERE username = ?""",
                (username,)
            )
            result = cursor.fetchone()
            print(f"Fetched security questions for {username}: {result}")

            if result:
                questions = {
                    1: result[0] or "",
                    2: result[1] or "",
                    3: result[2] or ""
                }
                answers = {
                    1: result[3] or "",
                    2: result[4] or "",
                    3: result[5] or ""
                }

                self.temp_questions = questions
                self.temp_answers = answers
                return {"questions": questions, "answers": answers}

            print("No security questions found for this user.")
            return None

        except sqlcipher3.Error as e:
            print(f"Error fetching security questions: {e}")
            return None

    def verify_security_answers(self, username, user_answers):
        """
        Verifies if the provided security answers match the stored ones.
        :param username: User's username.
        :param user_answers: Dictionary containing answers to security questions.
        :return: True if answers match, False otherwise.
        """
        data = self.get_security_questions(username)
        if not data:
            print(f"Security questions not found for username {username}.")
            return False  

        stored_answers = data["answers"]
        for key in stored_answers:
            if stored_answers[key] != user_answers.get(key, ""):
                print(f"Answer mismatch for question {key}.")
                return False

        print("All answers verified successfully.")
        return True

    def get_user_password_hash(self, username):
        """Retrieve the hashed password for a given user."""
        username = username.strip() if isinstance(username, str) else None
        if not username:
            return None

        try:
            cursor = self.db.cursor()
            cursor.execute(
                """SELECT password_hash FROM users WHERE username = ?""",
                (username,)
            )
            result = cursor.fetchone()
            print(f"Fetched password hash for {username}: {result}")
            return result[0] if result else None
        except sqlcipher3.Error as e:
            print(f"Database error while fetching user password: {e}")
            return None

    def update_user_password(self, username, new_password):
        """
        Securely updates the user's password after hashing.
        :param username: The user's username.
        :param new_password: The new password in plain text.
        :return: True if update was successful, False otherwise.
        """
        username = username.strip() if isinstance(username, str) else None
        if not username or not new_password:
            return False

        try:
            hashed_password = self.ph.hash(new_password)  
            cursor = self.db.cursor()
            cursor.execute(
                """UPDATE users 
                   SET password_hash = ?, updated_at = CURRENT_TIMESTAMP 
                   WHERE username = ?""",
                (hashed_password, username)
            )
            self.db.commit()  
            print(f"Password update for {username} successful.")
            return cursor.rowcount > 0  
        except sqlcipher3.Error as e:
            print(f"Error updating password: {e}")
            return False

    def create_user(self, username, password_hash, security_question1, 
                    security_question2, security_question3, 
                    security_question1_answer, security_question2_answer, 
                    security_question3_answer):
        """Creates a new user in the database."""
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash, alerts_enabled, default_chart, weekly_reports,"
                "monthly_reports, yearly_reports, security_question1, security_question2, security_question3,"
                "security_question1_answer, security_question2_answer, security_question3_answer) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (username, password_hash, 1, 0, 0, 0, 0, security_question1, security_question2, security_question3, 
                 security_question1_answer, security_question2_answer, security_question3_answer)
            )
            self.db.commit_db()
            print(f"User {username} created successfully.")
            self.temp_info.clear()
            return(True)
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
