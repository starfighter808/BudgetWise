from argon2.exceptions import VerifyMismatchError, Argon2Error
from argon2 import PasswordHasher

class User:
    """
    This class handles user-related functionalities such as:
    - Creating new users in the database.
    - Retrieving user information (e.g., password hashes, security questions).
    - Verifying user login credentials (username and password).

    Attributes:
        db (object): The database instance used for interacting with the database.
        ph (PasswordHasher): The password hasher instance used for hashing and verifying passwords.
        temp_info (dict): A temporary dictionary to store user input during the creation process.
    """

    def __init__(self, db_instance):
        """
        Initializes the User object with a database instance and a password hasher.

        Arguments:
            db_instance (object): The database instance for interacting with the database.
        """
        self.db = db_instance  # The database instance to interact with the database
        self.ph = PasswordHasher()  # The Argon2 password hasher instance for password hashing and verification
        self.temp_info = {}  # Temporary storage for user input during account creation

    def create_user(self, username, password_hash, security_question1, 
                    security_question2, security_question3, 
                    security_question1_answer, security_question2_answer, 
                    security_question3_answer):
        """
        Creates a new user in the database with the provided details.

        This method checks if the username already exists. If the username is unique, 
        it inserts the user's details into the database.

        Arguments:
            username (str): The username for the new user.
            password_hash (str): The hashed password for the new user.
            security_question1 (str): The first security question for account recovery.
            security_question2 (str): The second security question for account recovery.
            security_question3 (str): The third security question for account recovery.
            security_question1_answer (str): The answer to the first security question.
            security_question2_answer (str): The answer to the second security question.
            security_question3_answer (str): The answer to the third security question.

        Returns:
            None
        """
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
            self.temp_info.clear()  # Clear the temporary user input data
        except Exception as e:
            print(f"Error creating user: {e}")  # Handle any errors during the user creation process

    def get_user_password_hash_in_db(self, username):
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

    def verify_password(self, provided_username, provided_password):
        """
        Verifies the user login credentials (username and password).

        This method checks the database for the stored password hash and compares it 
        with the provided password. It returns `None` if the user doesn't exist, 
        `True` if the credentials are correct, and `False` if the password is incorrect.

        Arguments:
            provided_username (str): The username entered by the user during login.
            provided_password (str): The password entered by the user during login.

        Returns:
            None/True/False: 
                None if the user is not found, 
                True if the provided password matches the stored hash, 
                False if the password doesn't match.
        """
        password_hash_from_db = self.get_user_password_hash_in_db(provided_username)  # Fetch the stored password hash

        if password_hash_from_db is None:  # User not found in the database
            print("User not found")
            return None  # Return None to indicate the user doesn't exist
        try:
            # Verify the provided password matches the stored hash using Argon2
            return self.ph.verify(password_hash_from_db, provided_password)
        except VerifyMismatchError:  # If the password does not match the hash, return False
            return False
        except Argon2Error as e:  # Handle any Argon2-related errors during password verification
            print(f"Error verifying password: {e}")
            return False

    def hash_input(self, pwd: str) -> str:
        """
        Hashes the provided password using the Argon2 algorithm.

        Arguments:
            pwd (str): The plaintext password to be hashed.

        Returns:
            str: The hashed password.
        """
        return self.ph.hash(pwd)  # Return the hashed password using Argon2

    def get_user_security_questions(self, username):
        """
        Retrieves the security questions associated with a user for account recovery purposes.

        Arguments:
            username (str): The username for which we need to retrieve the security questions.

        Returns:
            tuple or None: A tuple containing the three security questions if the user is found, 
                            otherwise None if an error occurs or the user does not exist.
        """
        try:
            cursor = self.db.cursor()  # Create a cursor to interact with the database
            cursor.execute(
                "SELECT security_question1, security_question2, security_question3,"
                 "security_question1_answer, security_question2_answer, security_question3_answer" 
                 "FROM users WHERE username = ?", 
                (username,)
            )
            return cursor.fetchone()  # Return the security questions as a tuple or None if not found
        except Exception as e:
            print(f"Error retrieving security questions: {e}")  # Handle any errors that occur during the query
            return None  # Return None if an error occurs or the user doesn't exist
