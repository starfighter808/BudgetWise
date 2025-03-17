# TODO: remove get_user_id and related functions
import re
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, Argon2Error
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
        self.temp_username ={} # for other generic situations like forgot password
        self.temp_sign_up_data = {} # For the sing up process data
        self.temp_questions = {}
        self.temp_answers = {}

    ### ---- PASSWORD MANAGEMENT ---- ###

    def hash_password(self, password: str) -> str:
        """Hashes a password using Argon2 before storing it."""
        return self.ph.hash(password)
    
    def verify_password(self, username: str, provided_password: str) -> bool:
        """
        Verifies a user's password against the stored hash in the database.

        Args:
            username (str): The username of the user.
            provided_password (str): The password provided by the user for verification.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        password_hash_from_db = self.get_user_password_hash(username)

        if password_hash_from_db is None:
            return False  # User not found or error retrieving hash

        try:
            return self.ph.verify(password_hash_from_db, provided_password)
        except VerifyMismatchError:
            return False  # Incorrect password
        except Argon2Error as e:
            print(f"Error verifying password: {e}")
            return False  # Hashing failure

    def is_valid_password(self, password: str) -> bool:
        """
        Checks if a password meets security complexity requirements.

        Args:
            password (str): The password to validate.

        Returns:
            bool: True if the password is valid, False otherwise.
        """
        return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', password))
    
    ### ---- USER ACCOUNT MANAGEMENT ---- ###
    def create_user(self):
        
        username = self.temp_sign_up_data.get("username") 
        password_hash = self.temp_sign_up_data.get("password_hash")
        security_question1 = self.temp_sign_up_data.get("security_question1")
        security_question2 = self.temp_sign_up_data.get("security_question2")
        security_question3 = self.temp_sign_up_data.get("security_question3")           
        security_question1_answer = self.temp_sign_up_data.get("security_question1_answer")
        security_question2_answer = self.temp_sign_up_data.get("security_question2_answer") 
        security_question3_answer = self.temp_sign_up_data.get("security_question3_answer")

        try:
            cursor = self.db.cursor()  # Create a cursor to interact with the database
            cursor.execute(
                "INSERT INTO users (username, password_hash, alerts_enabled, default_chart, weekly_reports,"
                "monthly_reports, yearly_reports, security_question1, security_question2, security_question3,"
                "security_question1_answer, security_question2_answer, security_question3_answer) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (username, password_hash, 1, 0, 0, 0, 0, security_question1, security_question2, security_question3, 
                security_question1_answer, security_question2_answer, security_question3_answer)
            )  # Insert the new user's information into the 'users' table
            self.db.commit_db()  # Commit the changes to the database
            self.temp_sign_up_data.clear()  # Clear the temporary user input data
            return True
        except Exception as e:
            print(f"Error creating user: {e}")  # Handle any errors during the user creation process
            return False

    def get_user_by_username(self, username):
        if not username:
            return None

        try:
            cursor = self.db.cursor()
            cursor.execute(
                """SELECT username
                   FROM users WHERE username = ?""",
                (username,)
            )
            result = cursor.fetchone()

            if result:
                self.temp_username = {"username":result[0]}
                return {
                    "username": result[0]
                }
            return None
        except sqlcipher3.Error as e:
            print(f"Error fetching user by username: {e}")
            return None

    def update_user_password(self, username, new_password):
        """
        Securely updates a user's password after hashing.

        Args:
            username (str): The username of the user whose password needs to be updated.
            new_password (str): The new password.

        Returns:
            bool: True if the password was successfully updated, False otherwise.
        """
        if not username or not new_password:
            return False

        try:
            hashed_password = self.hash_password(new_password)
            cursor = self.db.cursor()
            cursor.execute(
                """UPDATE users 
                   SET password_hash = ?, updated_at = CURRENT_TIMESTAMP 
                   WHERE username = ?""",
                (hashed_password, username)
            )
            self.db.commit_db()
            print(f"Password updated successfully for {username}.")
            return cursor.rowcount > 0  # Returns True if any row was updated
        except sqlcipher3.Error as e:
            print(f"Error updating password: {e}")
            return False
        
    def get_user_password_hash(self, username):
            """
            Retrieves the stored password hash for a user from the database based on the provided username.

            Arguments:
                username (str): The username whose password hash is being retrieved.

            Returns:
                str or None: The password hash if the user exists, otherwise None if the user is not found.
            """
            try:
                cursor = self.db.cursor()  # Create a cursor to interact with the database
                cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
                result = cursor.fetchone()  # Fetch the password hash from the database
                return result[0] if result else None  # Return the password hash or None if the user doesn't exist
            except Exception as e:
                print(f"Error retrieving user credentials: {e}")  # Handle any errors during retrieval
                return None  # Return None if an error occurs or if the user is not found
            
### ---- SECURITY QUESTIONS ---- ###


    def get_security_questions(self):
        """
        Retrieve security questions for the user stored in temp_username.

        Returns:
            dict or None: A dictionary with the security questions or None if not found.
        """
        # Retrieve the stored username
        username = self.temp_username.get("username")

        if not username:
            print("Error: No username found in temp_username.")
            return None

        try:
            # Query the database for security questions
            cursor = self.db.cursor()
            cursor.execute(
                """SELECT security_question1, security_question2, security_question3,
                security_question1_answer, security_question2_answer, security_question3_answer
                FROM users WHERE username = ?""",
                (username,)
            )
            result = cursor.fetchone()

            # Return questions as a dictionary if found
            if result:
                self.temp_questions =  {"1": result[0], "2": result[1], "3": result[2]} 
                        
                self.temp_answers =  {"1": result[3], "2": result[4], "3": result[5]}
                
                return {"question1": result[0], "question2": result[1], "question3": result[2], 
                        "answer1": result[3], "answer2": result[4], "answer3": result[5]}
            else:
                print(f"Warning: No security questions found for username '{username}'.")
                return None

        except sqlcipher3.Error as e:
            print(f"Error fetching security questions: {e}")
            return None

    def verify_security_answer(self, question_key, user_answer):
        """
        Verifies if the provided answer matches the stored hashed answer for the selected question.
        """
        try:
            # Convert question_key to string to match stored dictionary keys
            question_key_str = str(question_key)

            # Debugging: Show stored answers and available keys
            print("Stored Answers:", self.temp_answers)
            print("Available Keys:", self.temp_answers.keys())
            print(f"Trying to access answer for question key: {question_key_str}")

            # Retrieve the hashed answer using the string key
            hashed_answer = self.temp_answers.get(question_key_str)

            if hashed_answer is None:
                print(f"No stored answer found for question key: {question_key_str}")
                return False

            print(f"Stored Hashed Answer for Key {question_key_str}: {hashed_answer}")  # Debugging

            # Verify answer using Argon2 (or your hashing method)
            return self.ph.verify(hashed_answer, user_answer)

        except VerifyMismatchError:
            print("Incorrect security answer.")
            return False  # Incorrect answer
        except ValueError:
            print("Invalid question key format.")
            return False
        except Exception as e:
            print(f"Unexpected error verifying security answer: {e}")
            return False

    ### ---- USER EXISTENCE CHECK ---- ###

    def username_exists(self, username: str) -> bool:
        """
        Checks if the provided username exists in the database.

        Args:
            username (str): The username to check for existence.

        Returns:
            bool: True if the username exists, False otherwise.
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(
                """SELECT 1 FROM users WHERE username = ? LIMIT 1""",
                (username,)
            )
            result = cursor.fetchone()
            return result is not None
        except sqlcipher3.Error as e:
            print(f"Error checking if username exists: {e}")
            return False

    def get_user_by_username(self, username):
        """Fetch user details by username (excluding sensitive data)."""
        self.username = username
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

    ## END OF NEW ##

    # TODO: this does not work. username is passed as ""
    def get_user_id(self, username):
        """
        Retrieve the user ID based on the username.
        
        Args:
            username (str): The username whose ID is to be fetched.

        Returns:
            int or None: The user ID if found, otherwise None.
        """
        if not isinstance(username, str) or not username.strip():
            print("Invalid username provided.")
            return None

        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT userID FROM users WHERE username = ?", (username.strip(),))
            result = cursor.fetchone()

            if result:
                return result[0]  # Return the user ID
            else:
                print(f"No user ID found for username: {username}")
                return None
        except sqlcipher3.Error as e:
            print(f"Database error while fetching user ID: {e}")
            return None
