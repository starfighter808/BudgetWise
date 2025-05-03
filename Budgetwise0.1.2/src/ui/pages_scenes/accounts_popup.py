import flet as ft
import datetime as dt
class MakeEdits(ft.AlertDialog):
    def __init__(self, user_data, colors):
        super().__init__()
        # Set the entire dialog's background color
        self.bgcolor = colors.GREY_BACKGROUND  # Use your desired darker color

        self.user_data = user_data
        self.colors = colors
        self.refresh = None
        self.userid = 1
        
        self.db = self.user_data.db
        self.cursor = self.db.cursor()

        # Initialize accounts and leftover amount
        self.budgets = []
        self.accounts = []
        self.current_account_id = 0
        self.leftover_amount = 9999.99
        self.total_allocated_amount = 9999.99
        self.budgetName = "PlaceHolder"
        self.budget_id = 0

        # Create a text widget to display budget information
        self.budget_info = ft.Text(
            f"Budget: {self.budgetName} (${self.total_allocated_amount}) - Leftover: ${self.leftover_amount}",
            size=16,
            color=self.colors.TEXT_COLOR,
        )

        # Create fields for account creation
        self.account_name_field = ft.TextField(
            label="Account Name",
            label_style=ft.TextStyle(color=self.colors.BORDERBOX_COLOR), 
            text_style=ft.TextStyle(color=self.colors.TEXT_COLOR),
            hint_text="Enter your account name",
            hint_style=ft.TextStyle(color=self.colors.BLUE_BACKGROUND),
            focused_border_color=self.colors.BORDERBOX_COLOR
        )

        self.account_allocated_field = ft.TextField(
            label="Account Allocated",
            label_style=ft.TextStyle(color=self.colors.BORDERBOX_COLOR), 
            keyboard_type=ft.KeyboardType.NUMBER,
            text_style=ft.TextStyle(color=colors.TEXT_COLOR),
            hint_text="Enter your allocated amount",
            hint_style=ft.TextStyle(color=colors.BLUE_BACKGROUND),
            focused_border_color= self.colors.BORDERBOX_COLOR
        )

        self.description_field = ft.TextField(
            label="Description",
            label_style=ft.TextStyle(color=self.colors.BORDERBOX_COLOR),  # sets the label color
            multiline=True,
            min_lines=1,
            max_lines=4,
            text_style=ft.TextStyle(color=colors.TEXT_COLOR),
            hint_text="What is this account for?",
            hint_style=ft.TextStyle(color=colors.BLUE_BACKGROUND),
            focused_border_color= self.colors.BORDERBOX_COLOR  # sets the outline color when focused
            # You can also try adding border_color="#93B8C8" if you want to change its default border color
        )


        # ListView to display added accounts
        self.accounts_list_view = ft.ListView(
            expand=True, spacing=5, padding=5, auto_scroll=False, height=150
        )

        # Build the dialog content. Remove extra padding in your container.
        self.content = ft.Container(
            width=500,
            bgcolor=self.bgcolor,
            content=ft.Column(
                spacing=10,
                controls=[
                    self.budget_info,
                    ft.Divider(),
                    ft.Text("Create account:", weight=ft.FontWeight.BOLD, color=self.colors.TEXT_COLOR),
                    ft.Row(
                        controls=[
                            ft.Container(self.account_name_field, expand=True),
                            ft.Container(self.account_allocated_field, expand=True),
                        ],
                        spacing=10,
                    ),
                    ft.Row(
                        controls=[
                        ],
                        spacing=10,
                    ),
                    self.description_field,
                    ft.Row(
                        controls=[ft.ElevatedButton("Add Account", on_click=self.add_account)],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Divider(),
                    ft.Text("Added accounts:", weight=ft.FontWeight.BOLD, color=self.colors.TEXT_COLOR),
                    ft.Container(
                        content=self.accounts_list_view,
                        height=200,
                        border=ft.border.all(1, self.colors.TEXT_COLOR),
                        padding=10,
                    ),
                ],
            ),
        )

        # Set up the dialog title and actions
        self.title = ft.Text("Add Budget Accounts", color=self.colors.TEXT_COLOR)
        self.actions = [
            ft.TextButton("Finish", on_click=self.close_dialog),
        ]
        self.actions_alignment = ft.MainAxisAlignment.END
    
    def update_leftover(self):
        # ... (same as before)
        total_allocated = sum(account["total_allocated_amount"] for account in self.accounts)
        self.leftover_amount = self.total_allocated_amount - total_allocated
        self.cursor.execute(
        "UPDATE budgets SET leftover_amount = ? WHERE user_id = ? AND budget_id = ?",
        (self.leftover_amount, self.userid, self.budget_id)
    )
        self.budget_info.value = (
            f"Budget: {self.budgetName} (${self.total_allocated_amount}) - "
            f"Leftover: ${self.leftover_amount}"
        )
        self.budget_info.update()

    def updateinfo(self, refresh):
        """Run initialization logic when the popup is displayed."""
        if self.user_data.user_id != 0:
            self.userid = self.user_data.user_id
        self.refresh = refresh
        self.update_budget_info()
        self.update_leftover()
        self.refresh_accounts_list()


        
    def update_budget_info(self):
        # Retrieve the list of budgets from the database.
        self.budgets = self.get_budget()
        
        if self.budgets:  # if there's at least one budget
            # Let’s assume you want to use the first budget returned.
            budget = self.budgets[0]
            self.budget_id = budget['budget_id']
            self.leftover_amount = budget['leftover_amount']
            self.total_allocated_amount = budget['total_budgeted_amount']
            # If your budget dictionary includes the budget name, update it; otherwise, use a default.
            self.budgetName = budget.get('budget_name', 'PlaceHolder')
        else:
            # If there are no budgets returned, you can keep defaults.
            self.leftover_amount = 0.0
            self.total_allocated_amount = 0.0
            self.budgetName = "PlaceHolder"

    def get_budget(self):
        self.cursor.execute("""
                SELECT budget_id, total_budgeted_amount, leftover_amount, budget_name
                FROM budgets
                WHERE user_id = ?
            """, (self.userid,)) 
        budgets = self.cursor.fetchall()

        return [
                {
                    'budget_id': account[0],
                    'total_budgeted_amount': account[1],
                    'leftover_amount': account[2],
                    'budget_name': account[3]
                }
                for account in budgets
            ]
    def get_accounts(self):
        # Get account information for the logged-in user
        self.cursor.execute("""
            SELECT budget_accounts_id, account_name, total_allocated_amount, notes
            FROM budget_accounts 
            WHERE user_id = ?
        """, (self.userid,))
        accounts = self.cursor.fetchall()

        current_month = dt.datetime.now().month
        current_year = dt.datetime.now().year

        results = []
        for account in accounts:
            budget_accounts_id = account[0]
            # Fetch just the 'amount' for transactions for the current month and year
            self.cursor.execute("""
                SELECT COALESCE(SUM(amount), 0)
                FROM transactions 
                WHERE budget_accounts_id = ? AND user_id = ?
                AND strftime('%m', transaction_date) = ? 
                AND strftime('%Y', transaction_date) = ?
            """, (budget_accounts_id, self.userid, f"{current_month:02d}", f"{current_year}"))
            total_transaction_amount = self.cursor.fetchone()[0]

            
            results.append({
                'budget_accounts_id': account[0],
                'account_name': account[1],
                'total_allocated_amount': account[2],
                'notes': account[3],
                'total_transaction_amount': total_transaction_amount  # sum of these amounts
            })

        return results



    
    def refresh_accounts_list(self):
        # Retrieve updated accounts from the DB every time this method is called.
        self.accounts = self.get_accounts()
        self.update_leftover()
        self.accounts_list_view.controls.clear()

        for account in self.accounts:
            # Define a callback to remove the account.
            def remove_account(e, account_id=account['budget_accounts_id']):
                # Delete the account from the DB (implement this function)
                self.delete_account_from_db(account_id)
                # Refresh the UI after deletion
                self.refresh_accounts_list()

            # Define a callback to edit the account.
            def edits_account(e, account_id=account['budget_accounts_id']):
                # Edit the account using its unique ID.
                self.edit_account(e, account_id)
                # Refresh the UI after editing
                self.refresh_accounts_list()

            # Create a UI row to display account information.
            account_row = ft.Row(
                controls=[
                    ft.Text(
                        # Displaying account name and allocated amount (from the DB)
                        f"{account['account_name']} - Allocated: ${account['total_allocated_amount']}",
                        expand=True,
                        color=self.colors.TEXT_COLOR,
                    ),
                    ft.IconButton(ft.Icons.EDIT, self.colors.GREEN_BUTTON, on_click=edits_account),
                    ft.IconButton(ft.Icons.DELETE, self.colors.ERROR_RED, on_click=remove_account),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
            self.accounts_list_view.controls.append(account_row)

        self.accounts_list_view.update()



    def add_account(self, e):
        # Retrieve and strip input values.
        name = self.account_name_field.value.strip()
        allocated_str = self.account_allocated_field.value.strip()
        description = self.description_field.value.strip()

        # Reset any previous error messages.
        self.account_name_field.error_text = None
        self.account_allocated_field.error_text = None

        if not name:
            self.account_name_field.error_text = "Account name cannot be empty"
            self.account_name_field.update()
            return

        # --- Duplicate Name Check ---
        # Exclude the current account if updating. Use lower-case comparison for case insensitivity.
        existing_names = [
            acct["account_name"].strip().lower()
            for acct in self.accounts
            if (not hasattr(self, "current_account_id") or acct["budget_accounts_id"] != self.current_account_id)
        ]
        if name.lower() in existing_names:
            self.account_name_field.error_text = "Account name already exists. Please choose a different name."
            self.account_name_field.update()
            return

        try:
            allocated = float(allocated_str)
        except ValueError:
            self.account_allocated_field.error_text = "Please enter a valid number"
            self.account_allocated_field.update()
            return

        # Check against leftover amounts.
        if hasattr(self, "current_account_id") and self.current_account_id is not None:
            # Retrieve the original allocated amount for the account being edited.
            original_allocated = next(
                (acct["total_allocated_amount"] for acct in self.accounts 
                if acct["budget_accounts_id"] == self.current_account_id), 0
            )
            # Calculate the effective leftover: leftover plus the original allocation.
            effective_leftover = self.leftover_amount + original_allocated
            if allocated > effective_leftover:
                self.account_allocated_field.error_text = f"Amount exceeds effective leftover (${effective_leftover})"
                self.account_allocated_field.update()
                return
            
            # --- New Checker for Transactions Total ---
            # Ensure that the new allocated amount is not lower than the sum of existing transactions.
            current_month = dt.datetime.now().month
            current_year = dt.datetime.now().year

            self.cursor.execute(
                """
                SELECT COALESCE(SUM(amount), 0)
                FROM transactions
                WHERE budget_accounts_id = ?
                AND strftime('%m', transaction_date) = ?
                AND strftime('%Y', transaction_date) = ?
                """,
                (self.current_account_id, f"{current_month:02d}", f"{current_year}")
            )
            transactions_sum = self.cursor.fetchone()[0]
            if allocated < transactions_sum:
                self.account_allocated_field.error_text = (
                    f"Allocated amount (${allocated}) cannot be less than the total transaction amount (${transactions_sum})."
                )
                self.account_allocated_field.update()
                return
        else:
            # For new accounts, perform the regular leftover check.
            if allocated > self.leftover_amount:
                self.account_allocated_field.error_text = f"Amount exceeds leftover (${self.leftover_amount})"
                self.account_allocated_field.update()
                return

        try:
            if hasattr(self, "current_account_id") and self.current_account_id is not None:
                # Update the existing account using its primary key.
                update_query = """
                    UPDATE budget_accounts
                    SET account_name = ?, total_allocated_amount = ?, notes = ?
                    WHERE budget_accounts_id = ?
                """
                update_params = (name, allocated, description, self.current_account_id)
                self.cursor.execute(update_query, update_params)
                print("Account updated.")
                # Clear the current_account_id state to switch back to insertion mode.
                self.current_account_id = None
            else:
                # Insert a new account.
                insert_query = """
                    INSERT INTO budget_accounts (user_id, budget_id, account_name, total_allocated_amount, notes)
                    VALUES (?, ?, ?, ?, ?)
                """
                insert_params = (self.userid, self.budget_id, name, allocated, description)
                self.cursor.execute(insert_query, insert_params)
                print("Account inserted.")

            self.db.commit_db()  # Commit the transaction.
        except Exception as ex:
            print("Error handling account:", ex)
            return

        # Update your leftover amount and refresh UI elements.
        self.update_leftover()
        self.refresh()
        self.refresh_accounts_list()

        # Clear the input fields.
        self.account_name_field.value = ""
        self.account_allocated_field.value = ""
        self.description_field.value = ""
        self.account_name_field.update()
        self.account_allocated_field.update()
        self.description_field.update()




    
    def delete_account_from_db(self, account):
        """Deletes an account if no related transactions exist and refreshes the table."""
        # Check for related transactions
        self.cursor.execute(
            "SELECT COUNT(*) FROM transactions WHERE budget_accounts_id = ?",
            (account,)
        )
        transaction_count = self.cursor.fetchone()[0]  # Get the count

        if transaction_count > 0:
            # Inform the user that the account can't be deleted
            error_message = f"Cannot delete account {account}. There are {transaction_count} related transactions."
            # Create and show a SnackBar with the error message.
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(error_message)
            )
            self.page.snack_bar.open = True
            self.page.update()
        else:
            # Proceed with deletion
            self.cursor.execute(
                "DELETE FROM budget_accounts WHERE budget_accounts_id = ? AND user_id = ?",
                (account, self.userid)
            )
            self.db.commit_db()
            self.refresh_accounts_list()
            self.refresh()
    
    def edit_account(self, e, account):
        # Refresh the accounts list in case it was updated
        self.refresh_accounts_list()
        
        # Find the specific account by ID
        self.current_account_id = account
        account = next((acct for acct in self.accounts if acct['budget_accounts_id'] == account), None)
        if account is None:
            print("Account not found.")
            return

        # Pre-fill the fields with the account's data
        self.account_name_field.value = account['account_name']
        self.account_allocated_field.value = str(account['total_allocated_amount'])
        self.description_field.value = account.get('notes')

        # Update UI fields so that changes are visible
        self.account_name_field.update()
        self.account_allocated_field.update()
        self.description_field.update()

        # Open the dialog for editing
        self.open_dialog()

        
    def close_dialog(self, e):
        self.refresh
        self.open = False
        self.update()

    def open_dialog(self):
        self.open = True
        self.update()
