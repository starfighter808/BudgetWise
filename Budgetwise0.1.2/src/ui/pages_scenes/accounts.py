import flet as ft
from datetime import datetime, timedelta
import json
from src.ui.pages_scenes.accounts_popup import MakeEdits
from src.ui.components.edit_budget import EditBudget

class Accounts(ft.View):
    def __init__(self, page: ft.Page, user_data, NavRail, colors):
        super().__init__(route="/accounts", bgcolor= colors.GREY_BACKGROUND)

        self.colors = colors
    
        self.controls.append(ft.Text("Accounts"))

        title_row = ft.Row( # This is the title of the page
        [
            ft.Text("Accounts", size=30, weight="bold", color = self.colors.TEXT_COLOR)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=False,
        )
        # Initialize the elements you need
        self.page = page
        self.user_data = user_data
        self.userid = None
        
        # Use the existing database connection from user_data
        self.db = self.user_data.db
        self.cursor = self.db.cursor()

        # Retrieve budget ID for the user
        self.budgetid = None 

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
        self.Add_accounts_button = ft.ElevatedButton(
            text="Add Account",
            on_click=lambda e: self.edits_button_clicked(e=None),
            width=200
        )
        # Add EditBudget popup and attach it to the overlay
        self.edit_budget_page = EditBudget(self.page, self.user_data, self.colors)
        self.page.overlay.append(self.edit_budget_page)

        self.edit_budget_button = ft.ElevatedButton(
            text="Edit Budget",
            on_click=self.open_edit_budget_popup,
            width=200
        )


        self.edits_page = MakeEdits(user_data, colors)
        self.page.overlay.append(self.edits_page)
        self.button_bar = ft.Row(
            controls=[
                self.generate_report_button,
                self.edit_budget_button,
                self.Add_accounts_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # or another alignment as needed
            spacing=10  # space between buttons
        )
        content = ft.Column(
            [
                title_row,
                self.button_bar,
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
    def did_mount(self):
        """Called when the view is first mounted."""
        self.updateinfo()
    
    def updateinfo(self):
        if self.user_data != 0:
            self.userid = self.user_data.user_id
        self.budgetid = self.user_data.budget_id
        self.edit_budget_page.updateinfo(refresh=self.updateinfo)
        self.edits_page.updateinfo(refresh=self.updateinfo)
        self.refresh_table()
        
    def open_edit_budget_popup(self, e):
        """Handle opening the Edit Budget popup."""
        self.edit_budget_page.open_dialog()
        self.page.update()



    def edits_button_clicked(self, e):
        """Handle the button click event and show the Accounts popup."""
        # Reset current_account_id since we are not editing an existing account.
        self.edits_page.current_account_id = None
        self.edits_page.refresh_accounts_list()
        self.edits_page.open_dialog()  # Open the Accounts popup dialog
        self.page.update()
    
    def update_button(self, e, account):
        """Handle the button click event and show the Reports popup with specific information to be editted."""
        self.edits_page.refresh_accounts_list()
        self.edits_page.edit_account(e, account) # Call the show() method of the Reports popup
        self.page.update()

    def refresh_table(self):
        """Updates the table dynamically and uses a custom meter to show overspending."""
        self.table.controls.clear()  # Clear the table for refresh

        # Table Header
        self.table.controls.append(ft.Row([
            ft.Text("Account", weight="bold", width=200, color=self.colors.BLUE_BACKGROUND, text_align="center", size=24),
            ft.Text("Balance", weight="bold", width=150, color=self.colors.BLUE_BACKGROUND, text_align="center", size=24),
            ft.Text("Allocation", weight="bold", width=300, color=self.colors.BLUE_BACKGROUND, text_align="center", size=24),
            ft.Text("Transactions", weight="bold", width=300, color=self.colors.BLUE_BACKGROUND, text_align="center", size=24),
            ft.Text("", width=50)  # Placeholder for delete button column
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10))

        accounts = self.get_accounts()
        for account in accounts:
            # Extract basic account information
            budget_accounts_id = account['budget_accounts_id']
            account_name = account['account_name']
            allocated_balance = account['total_allocated_amount']

            current_month = datetime.now().month
            current_year = datetime.now().year

            self.cursor.execute("""
                SELECT description, amount, transaction_date 
                FROM transactions 
                WHERE budget_accounts_id = ? AND user_id = ?
                AND strftime('%m', transaction_date) = ? 
                AND strftime('%Y', transaction_date) = ?
            """, (budget_accounts_id, self.userid, f"{current_month:02d}", f"{current_year}"))
            transactions = self.cursor.fetchall()


            # Use report_creation_dt to separate completed from scheduled transactions.
            report_creation_dt = datetime.now()  # or your specific report creation timestamp
            completed_total = 0.0
            # Prepare a list for displaying transactions (including scheduled status)
            display_transactions = []
            for description, amount, transaction_date in transactions:
                # Assume transaction_date is formatted as "YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS"
                transaction_dt = datetime.strptime(transaction_date.split()[0], "%Y-%m-%d")
                if transaction_dt <= report_creation_dt:
                    completed_total += amount
                    status = ""  # Transaction is finalized
                else:
                    status = "Scheduled"  # Future transaction
                display_transactions.append((description, amount, transaction_date, status))

            # Calculate updated balance using only completed transactions.
            updated_balance = allocated_balance - completed_total

            # Create the custom meter using the allocated and updated balances.
            custom_meter = self.create_custom_meter(allocated_balance, updated_balance, width=300, height=10)

            # Build the Sub-Table Header (adding a "Status" column if needed).
            sub_table_header = ft.Row(
                controls=[
                    ft.Text("Description", weight="bold", width=200, text_align="center",color=self.colors.GREEN_BUTTON, size=18),
                    ft.Text("Amount", weight="bold", width=150, text_align="center",color=self.colors.GREEN_BUTTON, size=18),
                    ft.Text("Transaction Date", weight="bold", width=200, text_align="center",color=self.colors.GREEN_BUTTON, size=18),
                    ft.Text("Status", weight="bold", width=100, text_align="center",color=self.colors.GREEN_BUTTON, size=18),
                ],
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )

            # Build the Sub-Table Rows for transactions.
            sub_table_rows = ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(description, width=200, text_align="center",color=self.colors.TEXT_COLOR, size=16),
                            ft.Text(f"${amount:.2f}", width=150, text_align="center",color=self.colors.TEXT_COLOR, size=16),
                            ft.Text(transaction_date, width=200, text_align="center",color=self.colors.TEXT_COLOR, size=16),
                            ft.Text(
                                status,
                                width=100,
                                text_align="center",
                                size=16,
                                color=self.colors.BLUE_BACKGROUND if status == "Scheduled" else self.colors.TEXT_COLOR,
                            ),
                        ],
                        spacing=0,
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ) for description, amount, transaction_date, status in display_transactions
                ],
                spacing=5,
            )

            # Wrap the sub-table in a Container (initially hidden)
            sub_table = ft.Container(
                content=ft.Column([sub_table_header, sub_table_rows]),
                visible=False,
                padding=10,
            )

            # Toggle Button for Sub-Table
            toggle_button = ft.ElevatedButton(
                text="View Transactions",
                on_click=lambda e, container=sub_table: self.toggle_sub_table(container),
                width=150
            )

            # Additional Buttons for edit and deletion.
            delete_button = ft.IconButton(
                icon=ft.Icons.DELETE,
                icon_color=self.colors.ERROR_RED,
                on_click=lambda e, a=budget_accounts_id: self.delete_account(a)
            )
            edit_button = ft.IconButton(
                icon=ft.Icons.EDIT,
                icon_color=self.colors.GREEN_BUTTON,
                on_click=lambda e, a=budget_accounts_id: self.update_button(e, a)
            )

            # Compose the account row. Instead of a standard progress bar we now show our custom_meter.
            account_row = ft.Row([
                ft.Text(account_name, width=200, color=self.colors.TEXT_COLOR, text_align="center", size=16),
                ft.Text(f"${updated_balance:.2f}", width=150, color=self.colors.TEXT_COLOR, text_align="center", size=16),
                ft.Container(content=custom_meter, alignment=ft.alignment.center, width=300),
                ft.Container(content=toggle_button, alignment=ft.alignment.center, width=300),
                ft.Container(content=edit_button, alignment=ft.alignment.center, width=50),
                ft.Container(content=delete_button, alignment=ft.alignment.center, width=50)
            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)

            # Combine the account row and the (initially hidden) sub-table.
            account_container = ft.Container(
                content=ft.Column([
                    account_row,
                    sub_table  # The transaction sub-table, which can be toggled.
                ]),
                padding=10
            )

            # Add the completed account container to the table.
            self.table.controls.append(account_container)

        self.table.update()  # Finally, update the table to refresh the UI.



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

    def create_custom_meter(self, allocated_balance, current_balance, width=300, height=10):
        """
        Returns a custom widget that simulates a progress bar which can show negative values.
        
        - For a positive or zero balance, a green bar fills to the right.
        - For a negative balance, a red bar extends to the left.
        """
        # Determine the positive (green) and negative (red) ratios.
        if current_balance >= 0:
            # A positive meter: fill the green portion up to the percentage of allocated_balance.
            positive_ratio = min(current_balance / allocated_balance, 1.0)
            negative_ratio = 0
        else:
            # If overspent, no green fill but a red bar proportional to the overspend.
            positive_ratio = 0
            negative_ratio = min(abs(current_balance) / allocated_balance, 1.0)

        # Base container that represents the full allocated balance.
        base_container = ft.Container(
            width=width,
            height=height,
            bgcolor=ft.Colors.GREY_300,
            border_radius=5,
        )

        # Green container (positive) fills from the left.
        positive_container = ft.Container(
            width=width * positive_ratio,
            height=height,
            bgcolor=ft.Colors.GREEN,
            border_radius=5,
            alignment=ft.alignment.center_left,
        )

        # Red container (negative) will visually represent overspending.
        # Note that using a Stack lets us overlay these containers.
        negative_container = ft.Container(
            width=width * negative_ratio,
            height=height,
            bgcolor=ft.Colors.RED,
            border_radius=5,
            alignment=ft.alignment.center_right,
        )

        # Use a Stack so that both effects are visible.
        meter = ft.Stack(
            controls=[
                base_container,
                positive_container,
                negative_container,
            ]
        )

        return meter


    def delete_account(self, account):
        """Deletes an account if no related transactions exist and refreshes the table."""
        # Check for related transactions
        self.cursor.execute(
            "SELECT COUNT(*) FROM transactions WHERE budget_accounts_id = ?",
            (account,)
        )
        transaction_count = self.cursor.fetchone()[0]  # Get the count

        if transaction_count > 0:
            # Build an error message.
            error_message = f"Cannot delete account {account}. There are {transaction_count} related transactions."
            # Create and show a SnackBar with the error message.
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(error_message)
            )
            self.page.snack_bar.open = True
            self.page.update()
        else:
            self.cursor.execute(
                "DELETE FROM budget_accounts WHERE budget_accounts_id = ? AND user_id = ?",
                (account, self.userid)
            )
            self.db.commit_db()
            self.refresh_table()
            self.edits_page.refresh_accounts_list()


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
                current_month = datetime.now().month
                current_year = datetime.now().year

                self.cursor.execute("""
                    SELECT description, amount, transaction_date 
                    FROM transactions 
                    WHERE budget_accounts_id = ? AND user_id = ?
                    AND strftime('%m', transaction_date) = ? 
                    AND strftime('%Y', transaction_date) = ?
                """, (budget_accounts_id, self.userid, f"{current_month:02d}", f"{current_year}"))
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