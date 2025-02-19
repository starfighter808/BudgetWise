import sqlcipher3 as s3
import string as str
import Database #This line imports the Database class to give us access to Database functions


#An important note to make when reviewing this code is to recognize that database variables have under_scores and local python variables do not
class Transaction:

    #inherit connection object from the database class
    def __init__(self, conn: Database):
        self.conn = conn

    def createTransaction(self, userID, budgetID, catID, vendorID, transAmount, description):
        try:
            #this query should create a transaction in the database
            query = """INSERT INTO transaction (user_id, budget_accounts_id, category_id, vendor_id, transaction_type, amount, description, recurring, importance_rating) VALUES (?,?,?,?,?,?,?,?,?)"""
            self.conn.execute(query, (userID, budgetID, catID, vendorID, """transaction_type_object""", transAmount, description, 0, 3)) #WARNING TRANSACTION_TYPE_OBJECT NOT FINAL
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in createTransaction: {e}")

    def getTransactionDetails(self, transactionID):
        try:
            #this query should return all of the details related to a single specific transaction_id
            query = """SELECT budget_accounts_id, category_id, vendor_id, transaction_type, amount, description, recurring, importance_rating FROM transactions WHERE transaction_id = ?"""
            return self.conn.fetchall(query,(transactionID))
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in getTransactionDetails: {e}")

    def getTransactionList(self, userID):
        try:
            #this query will return all of the transaction_ID's from a particular user_id
            query = """SELECT transaction_id FROM transactions WHERE user_id = ?"""
            return self.conn.fetchall(query,(userID))
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in getTransactionList: {e}")

    #def schedule_transaction()
    #more information required

    def delete_transaction(self, transactionID):
        try:
            #this query will delete the transaction with the associated transactionID
            query = """DELETE FROM transactions WHERE transaction_id = ?"""
            self.conn.execute(query, (transactionID))
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in delete_transaction: {e}")

    def getImportanceRating(self, transactionID):
        try:
            #this query will fetch the importance rating of a single transactionID
            query = """SELECT importance_rating FROM transactions WHERE transaction_id = ?"""
            return self.conn.fetchone(query,(transactionID))
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in getImportanceRating: {e}")

    def setImportanceRating(self, transactionID, transIR):
        try:
            #this query will fetch the importance rating of a single transactionID
            query = """UPDATE transactions SET importance_rating = ? WHERE transaction_id = ?"""
            return self.conn.fetchone(query, (transIR, transactionID))
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in setImportanceRating: {e}")

    def getRecurring(self, transactionID):
        try:
            #this query will fetch the importance rating of a single transactionID
            query = """SELECT recurring FROM transactions WHERE transaction_id = ?"""
            return self.conn.fetchone(query,(transactionID))
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in getRecurring: {e}")

    def setRecurring(self, transactionID, isRecurring):
        try:
            #this query will set the recurring boolean for a specific transaction_id
            query = """UPDATE transactions SET recurring = ? WHERE transaction_id = ?""" 
            self.conn.execute(query, (isRecurring, transactionID))
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in setRecurring: {e}")

    def getAmount(self, transactionID):
        try:
            #this query will fetch the amount of a specified transaction
            query = """SELECT amount FROM transactions WHERE transaction_id = ?"""
            return self.conn.fetchone(query, (transactionID))
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in getAmount: {e}")

    def setAmount(self, transactionID, transAmount):
        try:
            #this query will set the transaction amount related to the transactionid
            query = """UPDATE transactions SET amount = ? WHERE transaction_id = ?"""
            self.conn.execute(query, (transAmount, transactionID))
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in setAmount: {e}")

    def getDescription(self, transactionID):
        try:
            #this query will fetch the description related to the transactionid
            query = """SELECT description FROM transactions WHERE transaction_id = ?"""
            return self.conn.fetchone(query, (transactionID))
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in getDescription: {e}")

    def setDescription(self, transactionID, transDesc):
        try:
            #this query will set the description related to the transactionid
            query = """UPDATE transactions SET description = ? WHERE transaction_id = ?"""
            self.conn.execute(query, (transDesc, transactionID))
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in setDescription: {e}")

    def getDate(self, transactionID):
        try:
            #this query will return the date related to the transactionID
            query = """SELECT transaction_date FROM transactions WHERE transactionID = ?"""
            return self.conn.fetchone(query,(transactionID))
         # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in getDate: {e}")



