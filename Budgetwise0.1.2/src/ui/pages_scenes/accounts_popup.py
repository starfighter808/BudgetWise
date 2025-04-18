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
            text_style=ft.TextStyle(color=colors.TEXT_COLOR),
            hint_text="Enter your account name",
            hint_style=ft.TextStyle(color=colors.BLUE_BACKGROUND)
        )

        self.account_allocated_field = ft.TextField(
            label="Account Allocated", 
            keyboard_type=ft.KeyboardType.NUMBER,
            text_style=ft.TextStyle(color=colors.TEXT_COLOR),
            hint_text="Enter your allocated amount",
            hint_style=ft.TextStyle(color=colors.BLUE_BACKGROUND)
        )

        self.description_field = ft.TextField(
            label="Description", 
            multiline=True, 
            min_lines=1, 
            max_lines=4)

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
        print("I ran")
        if self.user_data.user_id != 0:
            self.userid = self.user_data.user_id
        self.refresh = refresh
        self.update_budget_info()
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
        print(budgets)

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
        # Include a WHERE clause to filter by user_id
        self.cursor.execute("""
            SELECT budget_accounts_id, account_name, total_allocated_amount
            FROM budget_accounts 
            WHERE user_id = ?
        """, (self.userid,))  # Use self.userid to fetch accounts specific to the logged-in user

        accounts = self.cursor.fetchall()
        return [{'budget_accounts_id': account[0], 'account_name': account[1], 'total_allocated_amount': account[2]} for account in accounts]
    def refresh_accounts_list(self):
        # Retrieve updated accounts from the DB every time this method is called.
        self.accounts = self.get_accounts()
        self.update_leftover()
        self.accounts_list_view.controls.clear()

        for account in self.accounts:
            # Define a callback to remove the account.
            # Note: we're capturing the unique account id (assuming it's available as 'budget_accounts_id')
            def remove_account(e, account_id=account['budget_accounts_id']):
                # Delete the account from the DB (you need to implement this function)
                self.delete_account_from_db(account_id)
                # Refresh the UI after deletion
                self.refresh_accounts_list()

            # Create a UI row to display account information.
            account_row = ft.Row(
                controls=[
                    ft.Text(
                        # Displaying account name and allocated amount (from the DB)
                        f"{account['account_name']} - Allocated: ${account['total_allocated_amount']}",
                        expand=True,
                    ),
                    ft.IconButton(ft.icons.DELETE, on_click=remove_account),
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

        try:
            allocated = float(allocated_str)
        except ValueError:
            self.account_allocated_field.error_text = "Please enter a valid number"
            self.account_allocated_field.update()
            return

        if allocated > self.leftover_amount:
            self.account_allocated_field.error_text = f"Amount exceeds leftover (${self.leftover_amount})"
            self.account_allocated_field.update()
            return

        # Build the account information dictionary.
        account = {
            "name": name,
            "total_allocated": allocated,
            "description": description,
        }

        # Instead of appending to self.accounts, insert the data into the database.
        try:
            # This example assumes you have a table `budget_accounts` with columns
            # account_name, total_allocated_amount, start_date, end_date, description, and user_id.
            insert_query = """
                INSERT INTO budget_accounts (user_id, budget_id, account_name, total_allocated_amount, notes)
                VALUES (?, ?, ?, ?, ?)
            """
            params = (
                self.userid,
                self.budget_id,
                account["name"],
                account["total_allocated"],
                account["description"],
            )
            self.cursor.execute(insert_query, params)
            self.db.commit_db()  # Ensure to commit the transaction.
        except Exception as ex:
            print("Error inserting account:", ex)
            return

        # Optionally, update your leftover amount here if needed.
        # For example, you might subtract allocated amount from leftover_amount and update the budget display.
        self.update_leftover()
        self.refresh()
        # Refresh the UI to display the current accounts directly from the DB.
        self.refresh_accounts_list()
        

        # Clear input fields.
        self.account_name_field.value = ""
        self.account_allocated_field.value = ""
        self.description_field.value = ""
        self.account_name_field.update()
        self.account_allocated_field.update()
        self.description_field.update()
    
    def delete_account_from_db(self, account):
        """Deletes an account and refreshes the table."""
        self.cursor.execute(
            "DELETE FROM budget_accounts WHERE budget_accounts_id = ? AND user_id = ?",
            (account, self.userid)
        )
        self.db.commit_db()
        self.refresh_accounts_list()
        self.refresh()
    
    def close_dialog(self, e):
        self.refresh
        self.open = False
        self.update()

    def open_dialog(self):
        self.open = True
        self.update()
