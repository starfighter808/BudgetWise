import flet as ft

class History(ft.View):
    def __init__(self, page: ft.Page, user_repo):
        super().__init__(route="/dashboard", bgcolor="#5C9DFF")
        
        # Initialize the elements you need
        self.user_repo = user_repo
        
        # Use the existing database connection from user_repo
        self.conn = self.user_repo.db
        self.cursor = self.conn.cursor()
        
        # Header
        self.header = ft.Container(
            content=ft.Text("Accounts", size=24, weight="bold", color=ft.colors.WHITE),
            alignment=ft.alignment.center,
            padding=20
        )
        
        # Table container, starts empty
        self.table = ft.Column(spacing=10)
        
        # Main Layout
        self.controls.extend([
            self.header,
            self.table
        ])
        
        self.refresh_table()  # Initial load

    def refresh_table(self):
        """Updates the table dynamically whenever accounts are changed."""
        self.table.controls.clear()

        # Table Header
        self.table.controls.append(ft.Row([
            ft.Text("Account", weight="bold", width=150, color=ft.colors.WHITE),
            ft.Text("Balance", weight="bold", width=100, color=ft.colors.WHITE),
            ft.Text("Allocation", weight="bold", width=250, color=ft.colors.WHITE),
            ft.Text("", weight="bold", width=50)  # Moved delete button over
        ]))

        accounts = self.get_accounts()
        if not accounts:
            self.table.controls.append(ft.Text("No accounts available.", italic=True, color=ft.colors.GREY_300))

        for account in accounts:
            account_name, balance = account['account_name'], account['balance']
            max_value = balance  # The progress bar max is the account balance

            # Create Progress Bar
            progress_bar = ft.ProgressBar(
                value=balance / max_value,
                width=250
            )

            # Delete Button (Now moved further right)
            delete_button = ft.IconButton(
                icon=ft.icons.DELETE,
                icon_color=ft.colors.RED_ACCENT,
                on_click=lambda e, a=account_name: self.delete_account(a)
            )

            # Add Row to Table
            self.table.controls.append(ft.Row([
                ft.Text(account_name, width=150, color=ft.colors.WHITE),
                ft.Text(f"${balance:.2f}", width=100, color=ft.colors.WHITE),
                progress_bar,
                ft.Container(delete_button, alignment=ft.alignment.center_right, width=50)
            ]))

        if self.page:
            self.table.update()

    def get_accounts(self):
        """Retrieves accounts from the budget_accounts table."""
        self.cursor.execute("SELECT account_name, balance FROM budget_accounts")
        rows = self.cursor.fetchall()
        accounts = [{'account_name': row[0], 'balance': row[1]} for row in rows]
        return accounts

    def delete_account(self, account):
        """Deletes an account and refreshes the table."""
        self.cursor.execute("DELETE FROM budget_accounts WHERE account_name = ?", (account,))
        self.conn.commit()
        self.refresh_table()
