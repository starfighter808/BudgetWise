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
        # Other temp info dictionary
        self.temp_budget = {}
        # Quick access
        self.user_id = 0
        self.username = ""
        self.budgets = []
        self.budget_name = ""
        self.budget_amount = 0.0
        self.budget_id = 0
        # For sign up process
        self.temp_sign_up_data = {}
        # Password reset process
        self.temp_questions = {}
        self.temp_answers = {}

    def is_valid_username(self, username):
        """Validates username to be at least 3 characters and alphanumeric."""
        return bool(re.match(r"^[a-zA-Z0-9]{3,}$", username))

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
            if self.ph.verify(password_hash_from_db, provided_password):
                self.username = username
                return(True)
        except VerifyMismatchError:
            return False  # Incorrect password
        except Argon2Error as e:
            print(f"Error verifying password: {e}")
            return False  # Hashing failure

    def is_valid_password(self, password: str) -> bool:
        # Modified regex: special characters are now optional
        return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&.#]{8,}$', password))
    
    ### ---- USER ACCOUNT MANAGEMENT ---- ###
    def create_user(self):
        
        self.username = self.temp_sign_up_data.get("username") 
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
                (self.username, password_hash, 1, 0, 0, 0, 0, security_question1, security_question2, security_question3, 
                security_question1_answer, security_question2_answer, security_question3_answer)
            )  # Insert the new user's information into the 'users' table
            self.db.commit_db()  # Commit the changes to the database
            self.temp_sign_up_data.clear()  # Clear the temporary user input data
            self.user_id = self.get_user_id(self.username)
            return True
        except Exception as e:
            print(f"Error creating user: {e}")  # Handle any errors during the user creation process
            return False

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
                   SET password_hash = ?
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
        Retrieve security questions for the user stored in username.

        Returns:
            dict or None: A dictionary with the security questions or None if not found.
        """
        # Retrieve the stored username
        if not self.username:
            print("Error: No username found in username.")
            return None

        try:
            # Query the database for security questions
            cursor = self.db.cursor()
            cursor.execute(
                """SELECT security_question1, security_question2, security_question3,
                security_question1_answer, security_question2_answer, security_question3_answer
                FROM users WHERE username = ?""",
                (self.username,)
            )
            result = cursor.fetchone()

            # Return questions as a dictionary if found
            if result:
                self.temp_questions =  {"1": result[0], "2": result[1], "3": result[2]} 
                        
                self.temp_answers =  {"1": result[3], "2": result[4], "3": result[5]}
                
                return {"question1": result[0], "question2": result[1], "question3": result[2], 
                        "answer1": result[3], "answer2": result[4], "answer3": result[5]}
            else:
                print(f"Warning: No security questions found for username '{self.username}'.")
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
        username = username.strip() if isinstance(self.username, str) else None
        if not username:
            return None

        try:
            cursor = self.db.cursor()
            cursor.execute(
                """SELECT user_id, username FROM users WHERE username = ?""",
                (username,)
            )
            result = cursor.fetchone()
            print(f"Fetched user result: {result}")
        except sqlcipher3.Error as e:
            print(f"Database error while fetching user: {e}")
            result = None

        return result  
    
    ## CREATE BUDGET##

    def create_budget(self, budget_name, budget_amount):
        try:            
            # Get user ID from the database
            cursor = self.db.cursor()

            # Insert the budget data into the budgets table
            cursor.execute(
                """INSERT INTO budgets (user_id, budget_name, total_budgeted_amount, leftover_amount, start_date, end_date) 
                VALUES (?, ?, ?, ?, DATE('now'), DATE('now', 'start of month', '+1 month', '-1 day'))""",
                (self.user_id, budget_name, budget_amount, budget_amount),
            )

            self.db.commit_db()
            print(f"Budget '{budget_name}' successfully added for user '{self.username}', at user_id '{self.user_id}', self.user_data.budget_name = , '{self.budget_name}', self.user_data.budget_amount = '{self.budget_amount}'.")
            return True

        except sqlcipher3.Error as e:
            print(f"Database error while inserting budget: {e}")
            return False
             

    def get_budget_id(self):
        """
        Retrieve the budget_id based on the username.
        
        Args:
            self.user_id (int): The users user_id that will be used to confirm the budget_id.
            self.budget_id (int): The users budget_id that is to be fetched.

        Returns:
            int or None: The budget_id if found, otherwise None.
        """
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT budget_id FROM budgets WHERE user_id = ? AND budget_name = ?", (self.user_id, self.budget_name))
            result = cursor.fetchone()

            if result:
                self.budget_id = result[0]
                print("budget_id stored in user_data = ", self.budget_id)
                return result[0]
            else:
                print(f"No budget found with name '{self.budget_name}' for user ID: {self.user_id}")
                return None
        except sqlcipher3.Error as e:
            print(f"Database error while fetching budget ID: {e}")
            return None

    ## END OF NEW ##

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
            cursor.execute("SELECT user_id FROM users WHERE username = ?", (username.strip(),))
            result = cursor.fetchone()

            if result:
                self.user_id = result[0]
                print("user id stored in user_data = ", self.user_id)
                return result[0]  # Return the user ID
            else:
                print(f"No user ID found for username: {username}")
                return None
        except sqlcipher3.Error as e:
            print(f"Database error while fetching user ID: {e}")
            return None


    def get_budget_accounts(self):
        """Fetch all budget accounts for the user and budget."""
        try:
            cursor = self.db.cursor()
            # Assuming you have a way to know the current budget_id
            # You might need to pass budget_id as an argument or store it in self
            cursor.execute("SELECT account_name FROM budget_accounts WHERE user_id = ?", (self.user_id,))
            return [row[0] for row in cursor.fetchall()]
        except sqlcipher3.Error as e:
            print(f"Database error while fetching budget accounts: {e}")
            return []

    def add_budget_account(self, budget_id, account_name, total_allocated_amount=0.0, current_amount=0.0, savings_goal=0.0, notes=None):
        """Add a budget account for the user."""
        try:
            cursor = self.db.cursor()
            cursor.execute(
                """INSERT INTO budget_accounts (user_id, budget_id, account_name, total_allocated_amount, current_amount, savings_goal, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (self.user_id, budget_id, account_name, total_allocated_amount, current_amount, savings_goal, notes),
            )
            self.db.commit_db()
            print(f"Budget account '{account_name}' successfully added.")
            return True
        except sqlcipher3.Error as e:
            print(f"Database error while adding budget account: {e}")
            return False

    def delete_budget_account(self, account_name):
        """Delete a budget account for the user."""
        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM budget_accounts WHERE user_id = ? AND account_name = ?", (self.user_id, account_name))
            self.db.commit_db()
            print(f"Budget account '{account_name}' successfully deleted.")
            return True
        except sqlcipher3.Error as e:
            print(f"Database error while deleting budget account: {e}")
            return False

    def update_budget_account_balance(self, account_name, new_balance):
        """Update the current balance of a specific budget account."""
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "UPDATE budget_accounts SET current_amount = ? WHERE user_id = ? AND account_name = ?",
                (new_balance, self.user_id, account_name),
            )
            self.db.commit_db()
            print(f"Budget account '{account_name}' current balance updated to {new_balance}.")
            return True
        except sqlcipher3.Error as e:
            print(f"Database error while updating budget account balance: {e}")
            return False

    def add_budget_accounts(self, budget_id, accounts):
        """Add multiple budget accounts at once based on the new data structure."""
        try:
            cursor = self.db.cursor()
            for account_data in accounts:
                cursor.execute(
                    """INSERT INTO budget_accounts (user_id, budget_id, account_name, total_allocated_amount, current_amount, savings_goal, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        self.user_id,
                        budget_id,
                        account_data.get("name"),
                        account_data.get("total_allocated", 0.0),
                        account_data.get("total_allocated", 0.0), # Assuming initial current amount is the allocated amount
                        account_data.get("savings_goal", 0.0),
                        account_data.get("description"),
                    ),
                )
            self.db.commit_db()
            print(f"Multiple budget accounts successfully added.")
            return True
        except sqlcipher3.Error as e:
            print(f"Database error while adding multiple budget accounts: {e}")
            return False


    def update_budget(self, name, amount):
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "UPDATE budgets SET budget_name = ?, total_budgeted_amount = ? WHERE budget_id = ? AND user_id = ?",
                (name, amount, self.budget_id, self.user_id)
            )
            self.db.commit_db()
            print("DB update committed.")

            self.budget_name = name
            self.budget_amount = amount
        except Exception as e:
            print(f"Database update failed: {e}")



    def get_budget_details(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT budget_id, budget_name, total_budgeted_amount FROM budgets WHERE user_id = ?", (self.user_id,))
            result = cursor.fetchone()

            if result:
                self.budget_id, self.budget_name, self.budget_amount = result
                print(f"Budget found: ID = {self.budget_id}, Name = {self.budget_name}, Amount = {self.budget_amount}")
                return self.budget_id, self.budget_name, self.budget_amount
            else:
                print(f"No budget found for user_id: {self.user_id}")
                self.budget_id = 0
                self.budget_name = ""
                self.budget_amount = 0
                return None

        except sqlcipher3.Error as e:
            print(f"Database error while fetching budget details: {e}")
            self.budget_id = 0
            self.budget_name = ""
            self.budget_amount = 0
            return None


    def get_all_budget_details(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT budget_id, budget_name, total_budgeted_amount FROM budgets WHERE user_id = ?", (self.user_id,))
            results = cursor.fetchall()

            self.budgets = results if results else []

            if self.budgets:
                print(f"{len(self.budgets)} budget(s) found for user_id: {self.user_id}")
                for budget in self.budgets:
                    print(f" - ID = {budget[0]}, Name = {budget[1]}, Amount = {budget[2]}")

                # Set first budget as default
                self.budget_id, self.budget_name, self.budget_amount = self.budgets[0]
                print(f"Default budget set to ID = {self.budget_id}, Name = {self.budget_name}, Amount = {self.budget_amount}")
            else:
                print(f"No budgets found for user_id: {self.user_id}")
                self.budget_id = self.budget_name = self.budget_amount = None

            return self.budgets

        except sqlcipher3.Error as e:
            print(f"Database error while fetching all budget details: {e}")
            self.budgets = []
            self.budget_id = self.budget_name = self.budget_amount = None
            return []


    def get_all_budget_accounts(self):
        """Fetch all budget accounts for the current user and budget, and store them in self.accounts."""
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "SELECT budget_accounts_id, account_name FROM budget_accounts WHERE user_id = ? AND budget_id = ?",
                (self.user_id, self.budget_id)
            )
            results = cursor.fetchall()
            self.account_names = results  # Store as list of tuples: [(id, name), ...]
            return self.account_names
        except sqlcipher3.Error as e:
            print(f"Database error while fetching all budget accounts: {e}")
            return []


        
