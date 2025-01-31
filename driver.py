from database import Database
from user import User

db = Database()
user_manager = User(db)
user_manager.create_user("Joe", "apassword123")
print(user_manager.get_user_id("Joe", "apassword123"))
db.close()