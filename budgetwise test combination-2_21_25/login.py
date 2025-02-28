from argon2 import PasswordHasher, exceptions
from user import User
from Database import Database

class Login:
    def __init__(self):
        self.ph = PasswordHasher()
        self.db = Database()  
        self.user_manager = User() 

    def verify_password(self, stored_hash, provided_password):
        try:
            self.ph.verify(stored_hash, provided_password)
            return True
        except exceptions.VerifyMismatchError:
            return False

    def login(self, user, pwd) -> str:
        user_record = self.pullUser(user)
        if user_record is None:
            print("User not found.")
            return None

        stored_username, stored_password = user_record
        if self.verify_password(stored_password, pwd):
            print("Login successful.")
            return stored_username
        else:
            print("Invalid password.")
            return None
        
    def signUp(self, user: str, pwd: str):
        hashed_pwd = self.hashInput(pwd)
        self.addUser(user, hashed_pwd)
    
    def hashInput(self, pwd: str) -> str:
        return self.ph.hash(pwd)
    
    def addUser(self, user: str, hashed_pwd: str):
        self.user_manager.create_user(user, hashed_pwd)

    def pullUser(self, stored_username: str):
        return self.user_manager.get_user_id(stored_username)
