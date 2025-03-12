import flet as ft
from datetime import datetime

class History(ft.View):
    def __init__(self, page: ft.Page, user_repo, NavRail):
        super().__init__(route="/history", bgcolor="#5C9DFF")
    
        self.controls.append(ft.Text("History"))

        title_row = ft.Row( # This is the title of the page
        [
            ft.Text("History", size=30, weight="bold")
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=False,
        )
        self.page = page
        self.user_repo = user_repo
        self.userid = self.user_repo.get_user_id(self.user_repo.username)
        
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


        combined_month_year_options = self.get_combined_month_year_options(self.cursor)
        self.combined_dropdown = self.create_combined_month_year_dropdown(combined_month_year_options)
        self.combined_dropdown.on_change = self.refresh_table


        content = ft.Column(
            [
                title_row,
                
                self.combined_dropdown,  # Dropdown for combined month-year

                # ----------------- PAGE CONTENT GOES BELOW -----------------

                ft.Text("Page Content", size=15, text_align=ft.TextAlign.CENTER),

                # ----------------- PAGE CONTENT GOES ABOVE -----------------
                self.scrollable_table
                
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
        # Refresh the dropdown each time the page is routed to
        self.refresh_combined_month_year_dropdown(self.cursor, self.combined_dropdown)

    def refresh_combined_month_year_dropdown(self, cursor, dropdown):
        # Get combined month-year options
        combined_month_year_options = self.get_combined_month_year_options(cursor)
        
        # Update Dropdown options
        dropdown.options = [ft.dropdown.Option(option) for option in combined_month_year_options]
        dropdown.update()

    def get_combined_month_year_options(self, cursor):
        cursor.execute("SELECT DISTINCT strftime('%Y-%m', transaction_date) FROM transactions")
        rows = cursor.fetchall()
        
        if not rows:
            return ["No data available"]
        
        # Convert to "Month Year" format
        month_year_options = []
        for row in rows:
            year, month = row[0].split('-')
            month_names = {
                '01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June',
                '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'
            }
            month_name = month_names[month]
            month_year_options.append(f"{month_name} {year}")
        
        return month_year_options

    
    def create_combined_month_year_dropdown(self, options):
        # Create Dropdown
        combined_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(option) for option in options],
            width=200,
            height=50,
            on_change=lambda e: print(f"Selected {e.control.value}")
        )
        return combined_dropdown

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
                    (self.userid, "Walmart")
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
                (self.userid, budget_accounts[4], vendors[0], 0, 300.00, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Fueling car', 0, 5)
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

    def refresh_table(self, e=None):
        """Updates the table dynamically based on the selected month and year."""
        selected_month_year = self.combined_dropdown.value
        print(f"Selected month-year: {selected_month_year}")  # Debug output

        if selected_month_year == "No data available":
            self.table.controls.clear()
            self.table.controls.append(ft.Text("No transactions available for the selected month and year.", italic=True, color=ft.colors.GREY_300, size=24))
            self.table.update()
            return

        try:
            selected_month, selected_year = self.parse_month_year(selected_month_year)
            print(f"Selected month: {selected_month}, Selected year: {selected_year}")  # Debug output
        except ValueError as ve:
            print(f"Error parsing selected month-year: {ve}")
            self.table.controls.clear()
            self.table.controls.append(ft.Text("Invalid date format selected.", italic=True, color=ft.colors.RED, size=24))
            self.table.update()
            return

        month_names = {
            'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
            'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'
        }
        
        selected_month = month_names.get(selected_month)
        if not selected_month:
            print(f"Invalid month selected: {selected_month}")
            self.table.controls.clear()
            self.table.controls.append(ft.Text("Invalid month selected.", italic=True, color=ft.colors.RED, size=24))
            self.table.update()
            return

        selected_date_prefix = f"{selected_year}-{selected_month}"

        self.insert_test_data()
        self.insert_test_vendors()
        self.insert_transaction_data()
        self.table.controls.clear()

        self.table.controls.append(ft.Row([
            ft.Text("Account", weight="bold", width=200, color=ft.colors.WHITE, text_align="center", size=24),
            ft.Text("Balance", weight="bold", width=150, color=ft.colors.WHITE, text_align="center", size=24),
            ft.Text("Allocation", weight="bold", width=300, color=ft.colors.WHITE, text_align="center", size=24),
            ft.Text("Transactions", weight="bold", width=300, color=ft.colors.WHITE, text_align="center", size=24),
            ft.Text("", weight="bold", width=50, size=24)
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10))

        accounts = self.get_accounts()
        if not accounts:
            self.table.controls.append(ft.Text("No accounts available.", italic=True, color=ft.colors.GREY_300, size=24))

        for account in accounts:
            budget_accounts_id, account_name, balance = account['budget_accounts_id'], account['account_name'], account['balance']
            max_value = balance

            self.cursor.execute("SELECT description, amount FROM transactions WHERE budget_accounts_id = ? AND strftime('%Y-%m', transaction_date) = ?", (budget_accounts_id, selected_date_prefix))
            transactions = self.cursor.fetchall()

            total_spent = sum(amount for _, amount in transactions)
            updated_balance = balance - total_spent

            dropdown_options = [f"{description}: ${amount:.2f}" for description, amount in transactions]
            dropdown = ft.Dropdown(
                options=[ft.dropdown.Option(option) for option in dropdown_options],
                width=300,
                height=50,
                on_change=lambda e, name=account_name: print(f"Selected {e.control.value} for account {name}")
            )

            progress_bar = ft.ProgressBar(
                value=updated_balance / max_value if max_value > 0 else 0,
                width=300,
                height=10
            )

            delete_button = ft.IconButton(
                icon=ft.icons.DELETE,
                icon_color=ft.colors.RED_ACCENT,
                on_click=lambda e, a=account_name: self.delete_account(a)
            )

            self.table.controls.append(ft.Row([
                ft.Text(account_name, width=200, color=ft.colors.WHITE, text_align="center", size=16),
                ft.Text(f"${updated_balance:.2f}", width=150, color=ft.colors.WHITE, text_align="center", size=16),
                ft.Container(content=progress_bar, alignment=ft.alignment.center, width=300),
                ft.Container(content=dropdown, alignment=ft.alignment.center, width=300),
                ft.Container(delete_button, alignment=ft.alignment.center_right, width=50)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10))

        if self.page:
            self.table.update()

    def parse_month_year(self, month_year):
        """Parse the combined month-year string and return month and year."""
        parts = month_year.split()
        if len(parts) != 2:
            raise ValueError("Invalid format")
        month, year = parts
        return month, year




    def get_accounts(self):
        self.cursor.execute("SELECT budget_accounts_id, account_name, balance FROM budget_accounts")
        accounts = self.cursor.fetchall()
        return [{'budget_accounts_id': account[0], 'account_name': account[1], 'balance': account[2]} for account in accounts]


    def delete_account(self, account):
        """Deletes an account and refreshes the table."""
        self.cursor.execute("DELETE FROM budget_accounts WHERE account_name = ?", (account,))
        self.db.commit_db()
        self.refresh_table()