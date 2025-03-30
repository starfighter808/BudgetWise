import flet as ft
from datetime import datetime, timedelta
import json

class Accounts(ft.View):
    def __init__(self, page: ft.Page, user_data, NavRail, colors):
        super().__init__(route="/accounts", bgcolor= colors.BLUE_BACKGROUND)

        self.colors = colors
    
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
        self.user_data = user_data
        # TODO: Store userid AFTER user has logged in
        self.userid = 1
        # self.userid = self.user_data.get_user_id(self.user_data.username)
        
        # Use the existing database connection from user_data
        self.db = self.user_data.db
        self.cursor = self.db.cursor()

        # Retrieve budget ID for the user
        self.budgetid = 1 

        self.table = ft.Column(spacing=10, alignment=ft.MainAxisAlignment.CENTER)

        # Scrollable wrapper specifically for the dynamic table elements
        self.TableElements = ft.ListView(
            controls=[
                self.table,  # Add your table elements here
            ],
            expand=True,
            spacing=10,
        )

        # Wrap the scrollable container
        self.scrollable_table = ft.Container(
            content=self.TableElements,  # Scrollable content
            expand=True,
            padding=10,
        )
        self.generate_report_button = ft.ElevatedButton(
            text="Generate Report",
            on_click=lambda e: self.store_report(),
            width=200
        )

        content = ft.Column(
            [
                title_row,

                # ----------------- PAGE CONTENT GOES BELOW -----------------

                self.scrollable_table,
                # ft.Text("Page Content", size=15, text_align=ft.TextAlign.CENTER),
                self.generate_report_button,

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
    def did_mount(self):
        """Called when the view is first mounted."""
        if self.user_data != 0:
            self.userid = self.user_data.user_id
        
        self.budgetid = self.get_budget_id(self.userid)
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
                """SELECT budget_id
                   FROM budgets WHERE user_id = ?""",
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
            INSERT INTO budget_accounts (user_id, budget_id, account_name, account_type, total_allocated_amount, savings_goal, notes, importance_rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            # Execute insert statements
            self.cursor.executemany(insert_query, test_data)
            self.db.commit_db()

        else:
            print("Data already exists in the budget_accounts table. Skipping insertion.")

    def insert_test_vendors(self):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM vendors")
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
                INSERT INTO vendors (user_id, vendor_name)
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
            self.cursor.execute("SELECT vendor_id FROM vendors")
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
            INSERT INTO transactions (user_id, budget_accounts_id, vendor_id, transaction_type, amount, transaction_date, description, recurring, importance_rating)
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
        self.table.controls.clear()  # Clear the table for refresh

        # Table Header
        self.table.controls.append(ft.Row([
            ft.Text("Account", weight="bold", width=200, color=self.colors.TEXT_COLOR, text_align="center", size=24),
            ft.Text("Balance", weight="bold", width=150, color=self.colors.TEXT_COLOR, text_align="center", size=24),
            ft.Text("Allocation", weight="bold", width=300, color=self.colors.TEXT_COLOR, text_align="center", size=24),
            ft.Text("Transactions", weight="bold", width=300, color=self.colors.TEXT_COLOR, text_align="center", size=24),
            ft.Text("", width=50)  # Placeholder for delete button column
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10))

        accounts = self.get_accounts()
        for account in accounts:
            budget_accounts_id, account_name, balance = account['budget_accounts_id'], account['account_name'], account['total_allocated_amount']

            # Calculate updated balance and transactions
            self.cursor.execute("""
                SELECT description, amount, transaction_date 
                FROM transactions 
                WHERE budget_accounts_id = ? AND user_id = ?
            """, (budget_accounts_id, self.userid))

            transactions = self.cursor.fetchall()
            

            # Limit the transactions to the most recent 10
            recent_transactions = transactions[:10] 

            total_spent = sum(amount for _, amount, _ in transactions)
            updated_balance = balance - total_spent

            # Allocation Progress Bar
            progress_bar = ft.ProgressBar(
                value=updated_balance / balance if balance > 0 else 0,
                width=300,
                height=10
            )

            # Sub-Table Header (Aligned Properly)
            sub_table_header = ft.Row(
                controls=[
                    ft.Text("Description", weight="bold", width=200, text_align="center", size=18),
                    ft.Text("Amount", weight="bold", width=150, text_align="center", size=18),
                    ft.Text("Transaction Date", weight="bold", width=200, text_align="center", size=18),
                ],
                spacing=0,  # No spacing here; maintain fixed widths
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )

            # Sub-Table Rows (Aligned with Header)
            sub_table_rows = ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(description, width=200, text_align="center", size=16),
                            ft.Text(f"${amount:.2f}", width=150, text_align="center", size=16),
                            ft.Text(updated_at, width=200, text_align="center", size=16),
                        ],
                        spacing=0,  # Ensure no extra horizontal spacing
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ) for description, amount, updated_at in recent_transactions
                ],
                spacing=5,  # Spacing between rows
            )

            # Full Sub-Table Wrapped in a Column
            sub_table = ft.Container(
                content=ft.Column(
                    controls=[sub_table_header, sub_table_rows],
                    spacing=10,  # Space between header and rows
                    alignment=ft.MainAxisAlignment.CENTER,  # Center all contents horizontally
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Align all contents vertically
                ),
                padding=10,
            )



            # Sub-Table (Hidden by Default)
            sub_table = ft.Container(
                content=ft.Column([sub_table_header, sub_table_rows]),
                visible=False,  # Initially hidden
                padding=10,
            )

            # Toggle Button for Sub-Table
            toggle_button = ft.ElevatedButton(
                text="View Transactions",
                on_click=lambda e, container=sub_table: self.toggle_sub_table(container),
                width=150
            )

            # Delete Button
            delete_button = ft.IconButton(
                icon=ft.icons.DELETE,
                icon_color= self.colors.ERROR_RED,
                on_click=lambda e, a=account_name: self.delete_account(a)
            )

            # Row Container
            account_container = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(account_name, width=200, color=self.colors.TEXT_COLOR, text_align="center", size=16),
                        ft.Text(f"${updated_balance:.2f}", width=150, color=self.colors.TEXT_COLOR, text_align="center", size=16),
                        ft.Container(content=progress_bar, alignment=ft.alignment.center, width=300),  # Re-added progress bar
                        ft.Container(content=toggle_button, alignment=ft.alignment.center, width=300),
                        ft.Container(content=delete_button, alignment=ft.alignment.center, width=50)
                    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                    sub_table  # Add sub-table directly beneath the account row
                ]),
                padding=10
            )

            # Add account container to the table
            self.table.controls.append(account_container)

        self.table.update()

    def toggle_sub_table(self, container):
        """Toggle visibility of a sub-table."""
        container.visible = not container.visible
        self.table.update()





    # TODO: Change the select statement to pull only budget_accounts tied to a specific user_id
    def get_accounts(self):
        # Include a WHERE clause to filter by user_id
        self.cursor.execute("""
            SELECT budget_accounts_id, account_name, total_allocated_amount
            FROM budget_accounts 
            WHERE user_id = ?
        """, (self.userid,))  # Use self.userid to fetch accounts specific to the logged-in user

        accounts = self.cursor.fetchall()
        return [{'budget_accounts_id': account[0], 'account_name': account[1], 'total_allocated_amount': account[2]} for account in accounts]



    def delete_account(self, account):
        """Deletes an account and refreshes the table."""
        self.cursor.execute("DELETE FROM budget_accounts WHERE account_name and user_id = ?", (account, self.userid,))
        self.db.commit_db()
        self.refresh_table()

    def store_report(self):
        """Store the table data as a report in the database."""
        try:
            # Prepare report data
            report_data = []

            # Gather data from the accounts table
            accounts = self.get_accounts()  # Assuming this method returns all accounts
            for account in accounts:
                budget_accounts_id, account_name, balance = account['budget_accounts_id'], account['account_name'], account['total_allocated_amount']

                # Calculate updated balance and transactions
                self.cursor.execute("""
                    SELECT description, amount, transaction_date 
                    FROM transactions 
                    WHERE budget_accounts_id = ? AND user_id = ?
                """, (budget_accounts_id, self.userid))
                transactions = self.cursor.fetchall()

                # Format account data with transactions
                account_data = {
                    "account_name": account_name,
                    "balance": balance,
                    "transactions": [
                        {"description": t[0], "amount": t[1], "date": t[2]} for t in transactions
                    ]
                }
                report_data.append(account_data)

            # Serialize the report data as JSON
            report_json = json.dumps(report_data)

            # Insert the report into the reports table
            self.cursor.execute("""
                INSERT INTO reports (user_id, report_type, report_data) 
                VALUES (?, ?, ?)
            """, (self.userid, 1, report_json))
            self.db.commit_db()

            print("Report stored successfully!")

        except Exception as e:
            print(f"An error occurred while storing the report: {e}")