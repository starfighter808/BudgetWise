import sqlcipher3 as s3
import string as str
import Database  

class Budget:

    def __init__(self, conn: Database):
        self.conn = conn

    def createBudget(self, budgetName, allocatedAmount, resetDate):
        try:
            # This query should create a budget in the database
            query = """INSERT INTO budget (budget_name, allocated_amount, reset_date) VALUES (?, ?, ?)"""
            self.conn.execute(query, (budgetName, allocatedAmount, resetDate))
        except s3.Error as e:
            print(f"An error occurred in createBudget: {e}")

    def deleteBudget(self, budgetID):
        try:
            # This query should delete the budget with the associated budgetID
            query = """DELETE FROM budget WHERE budget_id = ?"""
            self.conn.execute(query, (budgetID,))
        except s3.Error as e:
            print(f"An error occurred in deleteBudget: {e}")

    def updateAllocatedAmount(self, budgetID, newAmount):
        try:
            # This query should update the allocatedAmount of a specific budget
            query = """UPDATE budget SET allocated_amount = ? WHERE budget_id = ?"""
            self.conn.execute(query, (newAmount, budgetID))
        except s3.Error as e:
            print(f"An error occurred in updateAllocatedAmount: {e}")

    def resetBudget(self, budgetID):
        try:
            # This query should reset the allocated amount of a specific budget
            query = """UPDATE budget SET allocated_amount = 0 WHERE budget_id = ?"""
            self.conn.execute(query, (budgetID,))
        except s3.Error as e:
            print(f"An error occurred in resetBudget: {e}")

    def updateBudgetName(self, budgetID, newName):
        try:
            # This query should update the name of a specific budget
            query = """UPDATE budget SET budget_name = ? WHERE budget_id = ?"""
            self.conn.execute(query, (newName, budgetID))
        except s3.Error as e:
            print(f"An error occurred in updateBudgetName: {e}")

    def getBudgetByID(self, budgetID):
        try:
            # This query should fetch details of a specific budget based on the budgetID
            query = """SELECT * FROM budget WHERE budget_id = ?"""
            return self.conn.fetchone(query, (budgetID,))
        except s3.Error as e:
            print(f"An error occurred in getBudgetByID: {e}")

    def getBudgetByUser(self, userID):
        try:
            # This query should fetch all budgets associated with a specific userID
            query = """SELECT * FROM budget WHERE user_id = ?"""
            return self.conn.fetchall(query, (userID,))
        except s3.Error as e:
            print(f"An error occurred in getBudgetByUser: {e}")
