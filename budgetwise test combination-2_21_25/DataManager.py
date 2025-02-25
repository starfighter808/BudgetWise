class DataManager:
    def __init__(self):
        self.accounts = {}  # Dictionary to store accounts {name: value}
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
