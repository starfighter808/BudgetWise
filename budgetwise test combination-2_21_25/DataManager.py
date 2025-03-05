class DataManager:
    def __init__(self):
        self.accounts = {}  # Dictionary to store accounts {name: value}
        self.transactions = {}
        self.transaction_id_counter = 1
        self.listeners = []

    def add_listener(self, callback):
        """Registers a function to be called when data changes."""
        self.listeners.append(callback)

    def notify_listeners(self):
        """Calls all registered listener functions."""
        for listener in self.listeners:
            listener()

    def add_account(self, name, amount):
        """Adds or updates an account and notifies listeners."""
        if name and amount is not None:  # Ensure valid inputs
            self.accounts[name] = amount  # ✅ Directly update or add to dictionary
            print("Debug add_account():", self.accounts)  # 🔍 Debugging
            self.notify_listeners()

    def remove_account(self, name):
        """Removes an account if it exists."""
        if name in self.accounts:
            del self.accounts[name]  # ✅ Directly remove key from dictionary
            print("Debug remove_account():", self.accounts)  # 🔍 Debugging
            self.notify_listeners()

    def update_account(self, name, amount):
        """Updates an existing account's value."""
        if name in self.accounts:
            self.accounts[name] = amount  # ✅ Directly modify dictionary value
            print("Debug update_account():", self.accounts)  # 🔍 Debugging
            self.notify_listeners()

    def list_accounts(self):
        """Returns the dictionary of accounts."""
        print("Debug list_accounts():", self.accounts)  # 🔍 Debugging
        return self.accounts  # ✅ Returns dictionary instead of list of tuples
    
    def add_transaction(self, name, amount, date, account):
        """Adds a transaction and notifies listeners."""
        transaction = {
            "id": self.transaction_id_counter,  # ✅ Unique ID for every transaction
            "name": name,
            "amount": amount,
            "date": date,
            "account": account
        }
        
        # Store transaction using its unique ID as the key
        self.transactions[self.transaction_id_counter] = transaction  # ✅ Corrected

        self.transaction_id_counter += 1  # ✅ Increment ID for next transaction
        self.notify_listeners()

        return transaction["id"]  # ✅ Return the ID for reference

    def remove_transaction(self, name):
        """Removes a transaction by name and notifies listeners."""
        self.transactions = [t for t in self.transactions if t["name"] != name]
        print("Debug remove_transaction():", self.transactions)
        self.notify_listeners()

    def update_transaction(self, name, amount=None, date=None, account=None):
        """Updates a transaction and notifies listeners."""
        for transaction in self.transactions:
            if transaction["name"] == name:
                if amount is not None:
                    transaction["amount"] = amount
                if date is not None:
                    transaction["date"] = date
                if account is not None and account in self.accounts:
                    transaction["account"] = account
                print("Debug update_transaction():", transaction)
                self.notify_listeners()
                return
        print(f"Error: Transaction '{name}' not found!")

    def list_transactions(self):
        """Returns the list of transactions."""
        print("Debug list_transactions():", self.transactions)
        return self.transactions
