import flet as ft
from datetime import datetime, timedelta
import json
from src.ui.pages_scenes.accounts_popup import MakeEdits

class Accounts(ft.View):
    def __init__(self, page: ft.Page, user_data, NavRail, colors):
        super().__init__(route="/accounts", bgcolor= colors.GREY_BACKGROUND)

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
        self.userid = 1
        
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
        self.edits_page = MakeEdits(user_data, colors)
        self.page.overlay.append(self.edits_page)

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
        self.budgetid = self.user_data.budget_id
        self.edits_page.updateinfo(refresh=self.refresh_table)
        self.refresh_table()

    def edits_button_clicked(self, e):
        """Handle the button click event and show the Reports popup."""
        print("Show activated")
        self.edits_page.refresh_accounts_list()
        self.edits_page.open_dialog() # Call the show() method of the Reports popup
        self.page.update()
    
    
    def refresh_table(self):
        """Updates the table dynamically whenever accounts are changed."""
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
                icon=ft.Icons.DELETE,
                icon_color= self.colors.ERROR_RED,
                on_click=lambda e, a=account_name: self.delete_account(a)
            )

            edit_button = ft.IconButton(
                icon=ft.Icons.EDIT,
                icon_color= self.colors.GREEN_BUTTON,
                on_click=lambda e, a=account_name: self.edits_button_clicked(e=None)
            )

            # Row Container
            account_container = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(account_name, width=200, color=self.colors.TEXT_COLOR, text_align="center", size=16),
                        ft.Text(f"${updated_balance:.2f}", width=150, color=self.colors.TEXT_COLOR, text_align="center", size=16),
                        ft.Container(content=progress_bar, alignment=ft.alignment.center, width=300),  # Re-added progress bar
                        ft.Container(content=toggle_button, alignment=ft.alignment.center, width=300),
                        ft.Container(content=edit_button, alignment=ft.alignment.center, width=50),
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
        self.cursor.execute(
            "DELETE FROM budget_accounts WHERE account_name = ? AND user_id = ?",
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