import sqlcipher3 as s3
import string as str
import Database  

class BudgetAccount:

    def __init__(self, conn: Database):
        self.conn = conn

    def createBudgetAccount(self, budgetAccountName, allocatedAmount, accountType, accountName, accountBalance, savingsGoal=0.0, notes="", importanceRating=0):
        try:
            # This query should create a budget account in the database
            query = """INSERT INTO budget_accounts (budget_account_name, allocated_amount, account_type, account_name, account_balance, savings_goal, notes, importance_rating) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
            self.conn.execute(query, (budgetAccountName, allocatedAmount, accountType, accountName, accountBalance, savingsGoal, notes, importanceRating))
        except s3.Error as e:
            print(f"An error occurred in createBudgetAccount: {e}")

    def deleteBudgetAccount(self, budgetAccountID):
        try:
            # This query should delete the budget account with the associated budgetAccountID
            query = """DELETE FROM budget_accounts WHERE budget_account_id = ?"""
            self.conn.execute(query, (budgetAccountID,))
        except s3.Error as e:
            print(f"An error occurred in deleteBudgetAccount: {e}")

    def updateAccountBalance(self, budgetAccountID, newBalance):
        try:
            # This query should update the account balance of a specific budget account
            query = """UPDATE budget_accounts SET account_balance = ? WHERE budget_account_id = ?"""
            self.conn.execute(query, (newBalance, budgetAccountID))
        except s3.Error as e:
            print(f"An error occurred in updateAccountBalance: {e}")

    def updateAccountNotes(self, budgetAccountID, newNotes):
        try:
            # This query should update the notes of a specific budget account
            query = """UPDATE budget_accounts SET notes = ? WHERE budget_account_id = ?"""
            self.conn.execute(query, (newNotes, budgetAccountID))
        except s3.Error as e:
            print(f"An error occurred in updateAccountNotes: {e}")

    def updateImportanceRating(self, budgetAccountID, newRating):
        try:
            # This query should update the importance rating of a specific budget account
            query = """UPDATE budget_accounts SET importance_rating = ? WHERE budget_account_id = ?"""
            self.conn.execute(query, (newRating, budgetAccountID))
        except s3.Error as e:
            print(f"An error occurred in updateImportanceRating: {e}")

    def updateSavingsGoal(self, budgetAccountID, newGoal):
        try:
            # This query should update the savings goal of a specific budget account
            query = """UPDATE budget_accounts SET savings_goal = ? WHERE budget_account_id = ?"""
            self.conn.execute(query, (newGoal, budgetAccountID))
        except s3.Error as e:
            print(f"An error occurred in updateSavingsGoal: {e}")

    def getBudgetAccountByID(self, budgetAccountID):
        try:
            # This query should fetch details of a specific budget account based on the budgetAccountID
            query = """SELECT * FROM budget_accounts WHERE budget_account_id = ?"""
            return self.conn.fetchone(query, (budgetAccountID,))
        except s3.Error as e:
            print(f"An error occurred in getBudgetAccountByID: {e}")

    def getBudgetAccountByAccountName(self, accountName):
        try:
            # This query should fetch all budget accounts associated with a specific accountName
            query = """SELECT * FROM budget_accounts WHERE account_name = ?"""
            return self.conn.fetchall(query, (accountName,))
        except s3.Error as e:
            print(f"An error occurred in getBudgetAccountByAccountName: {e}")
