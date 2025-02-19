from argon2 import PasswordHasher, exceptions
from Database import database
from user import User

class Login:
    def __init__(self):
        self.ph = PasswordHasher()
        self.db = database("BudgetWise")  
        self.user_manager = User(self.db)

    def verify_password(self,stored_hash, provided_password):
        try:
            # This will raise an exception if the password doesn't match.
            self.ph.verify(stored_hash, provided_password)
            return True
        except exceptions.VerifyMismatchError:
            return False

    def login(self, user, pwd) -> str:
        username_password_tuple = self.pullUser(user)

        if username_password_tuple is None:
            print("user id is empty")
            return None

        stored_user_username = username_password_tuple[0]
        stored_user_password = username_password_tuple[1]

        if self.verify_password(stored_user_password, pwd):
            print("passsed the verify check")
            return stored_user_username
        else:
            print("failed the verify check")
            return None
        
    def signUp(self, user: str, pwd: str):
        # takeInput()
        # isUnique()
        hash = self.hashInput(pwd)
        self.addUser(user, hash)
    
    # hashes and returns password
    def hashInput(self, pwd: str) -> str:
        return self.ph.hash(pwd)
    
    # creates User object and adds new user to database
    def addUser(self, user: str, hash: str):
        self.user_manager.create_user(user, hash)

    def pullUser(self, stored_username: str):
        userID = self.user_manager.get_user_id(stored_username)
        return userID


#
