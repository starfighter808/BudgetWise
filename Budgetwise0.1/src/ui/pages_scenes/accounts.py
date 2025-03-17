import flet as ft
from datetime import datetime, timedelta

class Accounts(ft.View):
    def __init__(self, page: ft.Page, user_repo, NavRail):
        super().__init__(route="/accounts", bgcolor="#5C9DFF")
    
        self.controls.append(ft.Text("Accounts"))

        title_row = ft.Row( # This is the title of the page
        [
            ft.Text("Accounts", size=30, weight="bold")
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=False,
        )
        # Initialize the elements you need
        self.page = page
        self.user_repo = user_repo
        # TODO: Store userid AFTER user has logged in
        self.userid = 1
        # self.userid = self.user_repo.get_user_id(self.user_repo.username)
        
        # Use the existing database connection from user_repo
        self.db = self.user_repo.db
        self.cursor = self.db.cursor()

        # Retrieve budget ID for the user
        self.budgetid = self.get_budget_id(self.userid)

        # Table container, starts empty
        self.table = ft.Column(spacing=10, alignment=ft.MainAxisAlignment.CENTER)  # Center the table content

        # Wrap the table in a ListView for scrolling
        self.scrollable_table = ft.ListView(
            controls=[self.table],
            expand=True,
            spacing=10,
            padding=10,
        )

        content = ft.Column(
            [
                title_row,

                # ----------------- PAGE CONTENT GOES BELOW -----------------

                self.scrollable_table,
                # ft.Text("Page Content", size=15, text_align=ft.TextAlign.CENTER),

                # ----------------- PAGE CONTENT GOES ABOVE ----------------- 
            ],
            expand=True,  # Make content expand to take the remaining space

        )

        self.controls = [
            ft.Row(
                [
                    NavRail.rail, # navigation bar
                    ft.VerticalDivider(width=1), # divider between navbar and page content
                    content,
                ],
                expand=True,
            )
                                
        ]
    
    # TODO: This function is currently not being called anywhere
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
                (self.userid, self.budgetid, 'Investment Account', 1, 5000.00, 20000.00, 'Investments in stocks and bonds', 4),
                (self.userid, self.budgetid, 'Bills', 0, 1500, 0, 'Monthly Bills', 5)
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

    def insert_test_vendors(self):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM vendor")
            count = self.cursor.fetchone()[0]
            
            if count == 0:
                # Sample data to insert into vendor table
                test_data = [
                    (self.userid, "Velero"),
                    (self.userid, "Home Depot"),
                    (self.userid, "McDonalds"),
                    (self.userid, "Premiere"),
                    (self.userid, "Walmart"),
                    (self.userid, "Byan Utilities")
                ]

                # SQL insert statement for vendor table
                insert_query = """
                INSERT INTO vendor (the_user, vendor_name)
                VALUES (?, ?)
                """
                
                # Execute insert statements
                self.cursor.executemany(insert_query, test_data)
                self.db.commit_db()

            else:
                print("Data already exists in the vendor table. Skipping insertion.")
                
        except Exception as e:
            print(f"An error occurred: {e}")

    def insert_transaction_data(self):
        self.cursor.execute("SELECT COUNT(*) FROM transactions")
        count = self.cursor.fetchone()[0]
        
        if count == 0:
            self.cursor.execute("SELECT vendor_id FROM vendor")
            vendors = [v[0] for v in self.cursor.fetchall()]
            
            self.cursor.execute("SELECT budget_accounts_id FROM budget_accounts")
            budget_accounts = [b[0] for b in self.cursor.fetchall()]

            # TODO: for demo. Needed to add a transaction that happened a week from now
            wkFrmNow = datetime.now() + timedelta(weeks=1)

            test_data = [
                (self.userid, budget_accounts[0], vendors[0], 0, 150.00, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Buying groceries', 0, 3),
                (self.userid, budget_accounts[1], vendors[1], 0, 200.00, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Buying home supplies', 0, 4),
                (self.userid, budget_accounts[2], vendors[2], 1, 15.00, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Eating out', 0, 2),
                (self.userid, budget_accounts[3], vendors[3], 0, 75.00, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Watching a movie', 0, 3),
                (self.userid, budget_accounts[4], vendors[4], 0, 120.00, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Buying electronics', 0, 5),
                (self.userid, budget_accounts[0], vendors[1], 1, 200.00, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Buying furniture', 1, 4),
                (self.userid, budget_accounts[1], vendors[2], 0, 20.00, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Buying snacks', 0, 2),
                (self.userid, budget_accounts[2], vendors[3], 0, 50.00, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Entertainment', 0, 3),
                (self.userid, budget_accounts[3], vendors[4], 1, 150.00, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Buying clothes', 1, 5),
                (self.userid, budget_accounts[4], vendors[0], 0, 300.00, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Fueling car', 0, 5),
                (self.userid, budget_accounts[5], vendors[5], 0, 300.00, wkFrmNow.strftime('%Y-%m-%d %H:%M:%S'), 'Gas payment', 1, 5)
            ]

            insert_query = """
            INSERT INTO transactions (the_user, budget_accounts_id, vendor_id, transaction_type, amount, transaction_date, description, recurring, importance_rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            # Execute insert statements
            self.cursor.executemany(insert_query, test_data)
            self.db.commit_db()


        else:
            print("Data already exists in the budget_accounts table. Skipping insertion.")

    def refresh_table(self):
        """Updates the table dynamically whenever accounts are changed."""
        self.insert_test_data()  # Insert test data when the table is refreshed
        self.insert_test_vendors()
        self.insert_transaction_data()
        self.table.controls.clear()

        # Table Header
        self.table.controls.append(ft.Row([
            ft.Text("Account", weight="bold", width=200, color=ft.colors.WHITE, text_align="center", size=24),
            ft.Text("Balance", weight="bold", width=150, color=ft.colors.WHITE, text_align="center", size=24),
            ft.Text("Allocation", weight="bold", width=300, color=ft.colors.WHITE, text_align="center", size=24),
            ft.Text("Transactions", weight="bold", width=300, color=ft.colors.WHITE, text_align="center", size=24),
            ft.Text("", weight="bold", width=50, size=24)  # Moved delete button over
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10))  # Add spacing between columns

        accounts = self.get_accounts()
        if not accounts:
            self.table.controls.append(
                ft.Container(
                    content=ft.Text("No accounts available.", italic=True, color=ft.colors.GREY_300, size=24),
                    alignment=ft.alignment.center,
                )
            )
            # self.table.controls.append(ft.Text("No accounts available.", italic=True, color=ft.colors.GREY_300, alignment=ft.alignment.center, size=24))

        for account in accounts:
            budget_accounts_id, account_name, balance = account['budget_accounts_id'], account['account_name'], account['balance']
            max_value = balance  # The progress bar max is the initial account balance

            # Fetch transactions for the current budget_accounts_id
            self.cursor.execute("SELECT description, amount FROM transactions WHERE budget_accounts_id = ?", (budget_accounts_id,))
            transactions = self.cursor.fetchall()

            # Calculate total amount spent
            total_spent = sum(amount for _, amount in transactions)
            updated_balance = balance - total_spent

            # Create Dropdown options based on transactions
            dropdown_options = [f"{description}: ${amount:.2f}" for description, amount in transactions]

            # Create Dropdown
            dropdown = ft.Dropdown(
                options=[ft.dropdown.Option(option) for option in dropdown_options],
                width=300,  # Set width to match the header
                height=50,  # Set a height to ensure arrow is inside the box
                on_change=lambda e, name=account_name: print(f"Selected {e.control.value} for account {name}")
            )

            # Create Progress Bar
            progress_bar = ft.ProgressBar(
                value=updated_balance / max_value if max_value > 0 else 0,
                width=300,
                height=10  # Make progress bar taller
            )

            # Delete Button (Now moved further right)
            delete_button = ft.IconButton(
                icon=ft.icons.DELETE,
                icon_color=ft.colors.RED_ACCENT,
                on_click=lambda e, a=account_name: self.delete_account(a)
            )

            # Add Row to Table
            self.table.controls.append(ft.Row([
                ft.Text(account_name, width=200, color=ft.colors.WHITE, text_align="center", size=16),
                ft.Text(f"${updated_balance:.2f}", width=150, color=ft.colors.WHITE, text_align="center", size=16),
                ft.Container(content=progress_bar, alignment=ft.alignment.center, width=300),
                ft.Container(content=dropdown, alignment=ft.alignment.center, width=300),  # Adjust width to match the header
                ft.Container(delete_button, alignment=ft.alignment.center_right, width=50)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10))  # Add spacing between columns

        if self.page:
            self.table.update()


    # TODO: Change the select statement to pull only budget_accounts tied to a specific user_id
    def get_accounts(self):
        self.cursor.execute("SELECT budget_accounts_id, account_name, balance FROM budget_accounts")
        accounts = self.cursor.fetchall()
        return [{'budget_accounts_id': account[0], 'account_name': account[1], 'balance': account[2]} for account in accounts]


    def delete_account(self, account):
        """Deletes an account and refreshes the table."""
        self.cursor.execute("DELETE FROM budget_accounts WHERE account_name = ?", (account,))
        self.db.commit_db()
        self.refresh_table()
