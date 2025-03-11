import flet as ft

class Accounts(ft.View):
    def __init__(self, page: ft.Page, user_repo):
        super().__init__(route="/Accounts", bgcolor="#5C9DFF")
        
        # Initialize the elements you need
        self.page = page
        self.user_repo = user_repo
        self.userid = self.user_repo.get_user_id(self.user_repo.username)
        
        # Use the existing database connection from user_repo
        self.db = self.user_repo.db
        self.cursor = self.db.cursor()

        # Retrieve budget ID for the user
        self.budgetid = self.get_budget_id(self.userid)
        
        # Header
        self.header = ft.Container(
            content=ft.Text("Accounts", size=24, weight="bold", color=ft.colors.WHITE),
            alignment=ft.alignment.center,
            padding=20
        )
        
        # Table container, starts empty
        self.table = ft.Column(spacing=10, alignment=ft.MainAxisAlignment.CENTER)  # Center the table content
        
        # Main Layout
        self.controls.extend([
            ft.Container(
                content=ft.Column([
                    self.header,
                    self.table
                ], spacing=20),
                alignment=ft.alignment.center  # Center the entire content
            )
        ])
        
        # Do not call refresh_table here
        # self.refresh_table()  # Initial load

    def did_mount(self):
        """Called when the view is first mounted."""
        self.refresh_table()

    def get_budget_id(self, user_id):
        """
        Retrieve the budget ID based on the user ID.
        Returns the budget ID if found, or None if no record is found.
        """
        if not user_id:
            return None

        try:
            self.cursor.execute(
                """SELECT budgetID
                   FROM budget WHERE the_user = ?""",
                (user_id,)
            )
            result = self.cursor.fetchone()
            
            # Check if a result was found and return the budget ID
            if result:
                budget_id = result[0]
                print(f"Fetched budget ID for user ID {user_id}: {budget_id}")
                return budget_id
            else:
                print(f"No budget ID found for user ID {user_id}")
                return None
        except Exception as e:
            print(f"An error occurred while fetching the budget ID for user ID {user_id}: {e}")
            return None
        
    def insert_test_data(self):
        """Insert test data into the budget_accounts table if it does not already exist."""
        # Check if the table is empty
        self.cursor.execute("SELECT COUNT(*) FROM budget_accounts")
        count = self.cursor.fetchone()[0]
        
        if count == 0:
            # Sample data to insert into budget_accounts table
            test_data = [
                (self.userid, self.budgetid, 'Emergency Fund', 0, 1500.00, 5000.00, 'Saving for emergencies', 5),
                (self.userid, self.budgetid, 'Travel Fund', 0, 2000.00, 3000.00, 'Saving for vacations', 4),
                (self.userid, self.budgetid, 'Retirement Fund', 1, 10000.00, 50000.00, 'Saving for retirement', 5),
                (self.userid, self.budgetid, 'Education Fund', 0, 2500.00, 10000.00, 'Saving for kids education', 3),
                (self.userid, self.budgetid, 'Investment Account', 1, 5000.00, 20000.00, 'Investments in stocks and bonds', 4)
            ]

            # SQL insert statement for budget_accounts table
            insert_query = """
            INSERT INTO budget_accounts (the_user, the_budget, account_name, account_type, balance, savings_goal, notes, importance_rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            # Execute insert statements
            self.cursor.executemany(insert_query, test_data)
            self.db.commit_db()
        else:
            print("Data already exists in the budget_accounts table. Skipping insertion.")

    def refresh_table(self):
        """Updates the table dynamically whenever accounts are changed."""
        self.insert_test_data()  # Insert test data when the table is refreshed
        self.table.controls.clear()

        # Table Header
        self.table.controls.append(ft.Row([
            ft.Text("Account", weight="bold", width=150, color=ft.colors.WHITE, text_align="center"),
            ft.Text("Balance", weight="bold", width=100, color=ft.colors.WHITE, text_align="center"),
            ft.Text("Allocation", weight="bold", width=250, color=ft.colors.WHITE, text_align="center"),
            ft.Text("", weight="bold", width=50)  # Moved delete button over
        ], alignment=ft.MainAxisAlignment.CENTER))  # Center the row content

        accounts = self.get_accounts()
        if not accounts:
            self.table.controls.append(ft.Text("No accounts available.", italic=True, color=ft.colors.GREY_300, alignment=ft.alignment.center))

        for account in accounts:
            account_name, balance = account['account_name'], account['balance']
            max_value = balance  # The progress bar max is the account balance

            # Create Progress Bar
            progress_bar = ft.ProgressBar(
                value=balance / max_value if max_value > 0 else 0,
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
                ft.Text(account_name, width=150, color=ft.colors.WHITE, text_align="center"),
                ft.Text(f"${balance:.2f}", width=100, color=ft.colors.WHITE, text_align="center"),
                progress_bar,
                ft.Container(delete_button, alignment=ft.alignment.center_right, width=50)
            ], alignment=ft.MainAxisAlignment.CENTER))  # Center the row content

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
        self.db.commit_db()
        self.refresh_table()
