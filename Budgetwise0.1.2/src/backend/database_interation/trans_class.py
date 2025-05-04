import sqlcipher3 as s3
from datetime import (
    date,
)  # this library allows us to get the current date on the user machine in order to allow transaction dating


# An important note to make when reviewing this code is to recognize that database variables have under_scores and local python variables do not
class TransClass:

    # inherit connection object from the user_data class
    def __init__(self, user_data):
        # Use the existing database connection from user_data
        self.user_data = user_data
        self.db = self.user_data.db
        self.conn = self.db.cursor()

    def createTransaction(
        self, userID, transtype, transAmount, description, status, date=date.today()
    ):
        try:
            formatted_date = date.strftime("%Y-%m-%d")
            # this query should create a transaction in the database
            query = """INSERT INTO transaction (user_id, budget_accounts_id, vendor_id, amount, description, recurring, transaction_date, status) VALUES (?,?,?,?,?,?,?,?,?,?,?)"""
            self.conn.execute(
                query,
                (
                    userID,
                    transtype,
                    transAmount,
                    description,
                    0,
                    3,
                    formatted_date,
                    status,
                ),
            )  # WARNING STATUS_TYPE_OBJECT NOT FINAL
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in createTransaction: {e}")

    def getBudgetAccountName(self, budget_account_id):
        query = """SELECT account_name FROM budget_accounts WHERE budget_accounts_id = ?"""
        self.conn.execute(query, (budget_account_id,))
        return self.conn.fetchone()[0]  # Assuming it returns a single result.


    def getTransactionDetails(self, transactionID):
        try:
            # this query should return all of the details related to a single specific transaction_id
            query = """SELECT budget_accounts_id, vendor_id, amount, description, recurring, transaction_date  FROM transactions WHERE transaction_id = ?"""
            self.conn.execute(query, (transactionID))
            return self.conn.fetchall()
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in getTransactionDetails: {e}")

    def getTransactionList(self, userID):
        try:
            # this query will return all of the transaction_ID's from a particular user_id
            query = """SELECT transaction_id FROM transactions WHERE user_id = ?"""
            self.conn.execute(query, (userID,))
            return self.conn.fetchall()
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in getTransactionList: {e}")

    def checkTransactionDate(self):
        try:
            # get todays date for comparison
            today = date.today()
            formatted_date = today.strftime("%Y-%m-%d")
            # this query will update all transactions including or before todays date to "processed" via status_type_object
            query = (
                """UPDATE transactions SET status = ? WHERE date < ? AND status = ?"""
            )
            self.conn.execute(query, (1, formatted_date, 2))  # update status
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in checkTransactionDate: {e}")

    def delete_transaction(self, transactionID):
        try:
            # this query will delete the transaction with the associated transactionID
            query = """DELETE FROM transactions WHERE transaction_id = ?"""
            self.conn.execute(query, (transactionID,))
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in delete_transaction: {e}")


    def getRecurring(self, transactionID):
        try:
            # this query will fetch the importance rating of a single transactionID
            query = """SELECT recurring FROM transactions WHERE transaction_id = ?"""
            self.conn.execute(query, (transactionID,))
            return self.conn.fetchone()
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in getRecurring: {e}")

    def setRecurring(self, transactionID, isRecurring):
        try:
            # this query will set the recurring boolean for a specific transaction_id
            query = """UPDATE transactions SET recurring = ? WHERE transaction_id = ?"""
            self.conn.execute(query, (isRecurring, transactionID))
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in setRecurring: {e}")

    def getAmount(self, transactionID):
        try:
            # this query will fetch the amount of a specified transaction
            query = """SELECT amount FROM transactions WHERE transaction_id = ?"""
            self.conn.execute(query, (transactionID,))
            return self.conn.fetchone()
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in getAmount: {e}")

    def setAmount(self, transactionID, transAmount):
        try:
            # this query will set the transaction amount related to the transactionid
            query = """UPDATE transactions SET amount = ? WHERE transaction_id = ?"""
            self.conn.execute(query, (transAmount, transactionID))
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in setAmount: {e}")

    def getDescription(self, transactionID):
        try:
            # this query will fetch the description related to the transactionid
            query = """SELECT description FROM transactions WHERE transaction_id = ?"""
            self.conn.execute(query, (transactionID,))
            return self.conn.fetchone()
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in getDescription: {e}")

    def setDescription(self, transactionID, transDesc):
        try:
            # this query will set the description related to the transactionid
            query = (
                """UPDATE transactions SET description = ? WHERE transaction_id = ?"""
            )
            self.conn.execute(query, (transDesc, transactionID))
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in setDescription: {e}")

    def getDate(self, transactionID):
        try:
            # this query will return the date related to the transactionID
            query = (
                """SELECT transaction_date FROM transactions WHERE transactionID = ?"""
            )
            self.conn.execute(query, (transactionID,))
            return self.conn.fetchone()
        # if sqlite3 throws, print error to screen.
        except s3.Error as e:
            print(f"An error occurred in getDate: {e}")

    def create_transaction(self, transaction_data):
        # Insert data into your 'transactions' table
        query = """
            INSERT INTO transactions (user_id, budget_accounts_id, vendor_id, amount, transaction_date, description, recurring)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            transaction_data['user_id'],
            transaction_data['budget_accounts_id'],
            transaction_data['vendor_id'],
            transaction_data['amount'],
            transaction_data['transaction_date'],
            transaction_data['description'],
            transaction_data['recurring']
        )
        self.db.execute(query, params)
        self.db.commit()
        print(f"Transaction created for user_id {transaction_data['user_id']}")


# New method to get account_id from account_name
    def create_transaction(self, account_id, vendor_id, transAmount, description, recurring, transaction_date=None, status=2):
        """
        Insert a new transaction into the database using account_id and vendor_id directly.
        User ID is fetched from self.user_data.user_id, and transaction_id is auto-incremented.
        """
        if transaction_date is None:
            transaction_date = date.today().strftime("%Y-%m-%d")

        try:
            cursor = self.db.cursor()
            cursor.execute(
                """INSERT INTO transactions (user_id, budget_accounts_id, vendor_id, amount, description, recurring, transaction_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    self.user_data.user_id,  # User ID fetched from self.user_data
                    account_id,
                    vendor_id,
                    transAmount,
                    description,
                    int(recurring),
                    transaction_date,
                    int(status)
                )
            )

            # Commit the changes to the database
            self.db.commit_db()  # Commit the transaction to the database
            print(f"Transaction created for user_id {self.user_data.user_id} with amount {transAmount}")
            return True

        except Exception as e:
            print(f"An error occurred in create_transaction: {e}")
            return False

    def update_transaction(self, transaction_id, account_id, vendor_id, transAmount, description, recurring, transaction_date=None, status=2):
        if transaction_date is None:
            transaction_date = date.today().strftime("%Y-%m-%d")

        try:
            cursor = self.db.cursor()
            cursor.execute(
                """UPDATE transactions
                SET budget_accounts_id = ?,
                    vendor_id = ?,
                    amount = ?,
                    description = ?,
                    recurring = ?,
                    transaction_date = ?,
                    status = ?
                WHERE transaction_id = ?""",
                (
                    account_id,
                    vendor_id,
                    transAmount,
                    description,
                    int(recurring),
                    transaction_date,
                    int(status),
                    transaction_id
                )
            )
            self.db.commit_db()
            print(f"Transaction updated for transaction_id {transaction_id} with new amount {transAmount}")
            return True

        except Exception as e:
            print(f"An error occurred in update_transaction: {e}")
            return False





    def get_account_id(self, account_name):
        try:
            cursor = self.db.cursor()
            cursor.execute(
                """SELECT budget_accounts_id FROM budget_accounts WHERE account_name = ?""",
                (account_name,)
            )
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"An error occurred in get_account_id: {e}")


    def get_vendor_id(self, vendor_name):
        try:
            cursor = self.db.cursor()
            cursor.execute(
                """SELECT vendor_id FROM vendors WHERE vendor_name = ?""",
                (vendor_name,)
            )
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"An error occurred in get_vendor_id: {e}")

