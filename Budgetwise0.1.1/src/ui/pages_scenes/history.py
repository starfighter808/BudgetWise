import flet as ft
from datetime import datetime

class History(ft.View):
    def __init__(self, page: ft.Page,user_data, NavRail, colors):
        super().__init__(route="/history", bgcolor= colors.BLUE_BACKGROUND)
    
        self.controls.append(ft.Text("History"))
        self.colors = colors

        title_row = ft.Row( # This is the title of the page
        [
            ft.Text("History", size=30, weight="bold")
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=False,
        )
        self.page = page
        self.user_repo =user_data
        self.userid = 1
        
        # Use the existing database connection fromuser_data
        self.db = self.user_repo.db
        self.cursor = self.db.cursor()

        # Retrieve budget ID for the user
        self.budgetid = 1

        # Table container, starts empty
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

        combined_month_year_options = self.get_combined_month_year_options(self.cursor)
        self.combined_dropdown = self.create_combined_month_year_dropdown(combined_month_year_options)
        self.combined_dropdown.on_change = self.refresh_table


        content = ft.Column(
            [
                title_row,
                self.combined_dropdown,  # Dropdown for combined month-year
                # ----------------- PAGE CONTENT GOES BELOW -----------------
                self.scrollable_table
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
        # Refresh the dropdown each time the page is routed to
        if self.user_repo.user_id != 0:
            self.userid = self.user_repo.user_id
        self.budgetid = self.get_budget_id(self.userid)
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
            #height=50,
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
                """SELECT budget_id
                   FROM budget WHERE user_id = ?""",
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
        
    def refresh_table(self, e=None):
        """Updates the table dynamically based on the selected month and year."""
        selected_month_year = self.combined_dropdown.value
        print(f"Selected month-year: {selected_month_year}")  # Debug output

        if selected_month_year == "No data available":
            self.table.controls.clear()
            self.table.controls.append(ft.Text("No transactions available for the selected month and year.", italic=True, color=self.colors.GREY_BACKGROUND, size=24))
            self.table.update()
            return

        try:
            selected_month, selected_year = self.parse_month_year(selected_month_year)
            print(f"Selected month: {selected_month}, Selected year: {selected_year}")  # Debug output
        except ValueError as ve:
            print(f"Error parsing selected month-year: {ve}")
            self.table.controls.clear()
            self.table.controls.append(ft.Text("Invalid date format selected.", italic=True, color=self.colors.ERROR_RED, size=24))
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
            self.table.controls.append(ft.Text("Invalid month selected.", italic=True, color=self.colors.ERROR_RED, size=24))
            self.table.update()
            return

        selected_date_prefix = f"{selected_year}-{selected_month}"

        self.table.controls.clear()

        # Table Header
        self.table.controls.append(ft.Row([
            ft.Text("Account", weight="bold", width=200, color=self.colors.TEXT_COLOR, text_align="center", size=24),
            ft.Text("Balance", weight="bold", width=150, color=self.colors.TEXT_COLOR, text_align="center", size=24),
            ft.Text("Allocation", weight="bold", width=300, color=self.colors.TEXT_COLOR, text_align="center", size=24),
            ft.Text("Transactions", weight="bold", width=300, color=self.colors.TEXT_COLOR, text_align="center", size=24),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10))

        accounts = self.get_accounts()
        if not accounts:
            self.table.controls.append(ft.Text("No accounts available.", italic=True, color=self.colors.GREY_BACKGROUND, size=24))

        for account in accounts:
            budget_accounts_id, account_name, balance = account['budget_accounts_id'], account['account_name'], account['balance']

            # Fetch transactions for the selected month and year
            self.cursor.execute("""
                SELECT description, amount, transaction_date 
                FROM transactions 
                WHERE budget_accounts_id = ? AND strftime('%Y-%m', transaction_date) = ?
            """, (budget_accounts_id, selected_date_prefix))

            transactions = self.cursor.fetchall()
            recent_transactions = transactions[:10]
            total_spent = sum(amount for _, amount, _ in transactions)
            updated_balance = balance - total_spent

            # Allocation Progress Bar
            progress_bar = ft.ProgressBar(
                value=updated_balance / balance if balance > 0 else 0,
                width=300,
                height=10
            )

            # Sub-Table Header
            sub_table_header = ft.Row(
                controls=[
                    ft.Text("Description", weight="bold", width=200, text_align="center", size=18),
                    ft.Text("Amount", weight="bold", width=150, text_align="center", size=18),
                    ft.Text("Transaction Date", weight="bold", width=200, text_align="center", size=18),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )

            # Sub-Table Rows
            sub_table_rows = ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(description, width=200, text_align="center", size=16),
                            ft.Text(f"${amount:.2f}", width=150, text_align="center", size=16),
                            ft.Text(transaction_date, width=200, text_align="center", size=16),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ) for description, amount, transaction_date in recent_transactions
                ]
            )

            # Sub-Table Container (Hidden by Default)
            sub_table = ft.Container(
                content=ft.Column([sub_table_header, sub_table_rows]),
                visible=False,
                padding=10,
            )

            # Toggle Button
            toggle_button = ft.ElevatedButton(
                text="View Transactions",
                on_click=lambda e, container=sub_table: self.toggle_sub_table(container),
                width=150
            )

            # Account Row Container
            self.table.controls.append(ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(account_name, width=200, color=self.colors.TEXT_COLOR, text_align="center", size=16),
                        ft.Text(f"${updated_balance:.2f}", width=150, color=self.colors.TEXT_COLOR, text_align="center", size=16),
                        ft.Container(content=progress_bar, alignment=ft.alignment.center, width=300),
                        ft.Container(content=toggle_button, alignment=ft.alignment.center, width=300),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    sub_table
                ]),
                padding=10
            ))

        self.table.update()

    def toggle_sub_table(self, container):
        """Toggle visibility of a sub-table."""
        container.visible = not container.visible
        self.table.update()


    def parse_month_year(self, month_year):
        """Parse the combined month-year string and return month and year."""
        parts = month_year.split()
        if len(parts) != 2:
            raise ValueError("Invalid format")
        month, year = parts
        return month, year



 # TODO: Change the select statement to pull only budget_accounts tied to a specific user_id
    def get_accounts(self):
        # Include a WHERE clause to filter by user_id
        self.cursor.execute("""
            SELECT budget_accounts_id, account_name, total_allocated_amount 
            FROM budget_accounts 
            WHERE user_id = ?
        """, (self.userid,))  # Use self.userid to fetch accounts specific to the logged-in user

        accounts = self.cursor.fetchall()
        return [{'budget_accounts_id': account[0], 'account_name': account[1], 'balance': account[2]} for account in accounts]