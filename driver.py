from database import Database
from user import User

conn = Database()
user_manager = User(conn)
user_manager.create_user("Joe", "apassword123")
print(user_manager.get_user_id("Joe", "apassword123"))
conn.close()
