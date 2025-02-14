from argon2 import PasswordHasher
from database import Database
from user import User

class Login:
    def __init__(self):
        self.ph = PasswordHasher()
        self.db = Database()
        self.user_manager = User(self.db)

    def login(self, user, pwd):
        # takeInput()
        hash = self.hashInput(pwd)
        # checkHash(hash)
        userID = self.pullUser(user, hash)
        return

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

    def pullUser(self, user: str, hash: str):
        userID = self.user_manager.get_user_id(user, hash)
        print(userID)
        return userID


# FOR TESTING
login = Login()
login.signUp("jim", "strongpassword")
login.login("Jim", "strongpassword")