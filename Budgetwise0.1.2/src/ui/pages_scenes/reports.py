import flet as ft
from datetime import datetime
import json

class Reports(ft.AlertDialog):
    def __init__(self, user_data, colors):
        super().__init__(modal=True)  # Initialize as an AlertDialog
        self.user_repo = user_data
        self.db = self.user_repo.db
        self.cursor = self.db.cursor()
        self.colors = colors

        self.userid = 1
        self.reports = []

        # Title Row
        title_row = ft.Row(
            [ft.Text("Reports", size=30, weight="bold")],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=False,
        )

        # Reports Table Container
        self.table = ft.Column(spacing=10, alignment=ft.MainAxisAlignment.CENTER)

        # Scrollable Wrapper for Table Content
        self.TableElements = ft.ListView(
            controls=[self.table],  # Dynamic table elements
            expand=True,
            spacing=10,
        )

        # Wrap the Scrollable Container
        self.scrollable_table = ft.Container(
            content=self.TableElements,
            expand=True,
            padding=10,
        )

        # Close Button
        self.close_button = ft.Container(
            content=ft.ElevatedButton(
                text="Close",
                on_click=lambda e: self.hide(),  # Call the hide() method
            ),
            alignment=ft.alignment.bottom_center,
            padding=10,
            expand=False,
        )

        # Refresh Button
        self.refresh_button = ft.Container(
            content=ft.ElevatedButton(
                text="Print",
                on_click=self.refresh_reports,
            ),
            alignment=ft.alignment.bottom_left,
            padding=10,
            expand=False,
        )

        # Main Content
        # Main Content
        self.content = ft.Container(
            content=ft.Column(
                [
                    title_row,
                    self.scrollable_table,  # Scrollable table
                    self.refresh_button,  # Fixed Refresh Button
                    self.close_button,  # Close Button
                ],
                expand=True,
                spacing=20,
            ),
            padding=20,
            bgcolor=self.colors.BLUE_BACKGROUND,
            expand=True,
            width=960,
            height=960  # Set the desired width (e.g., 800 pixels)
        )


    def show(self):
        """Show the popup."""
        print("Activation Recieved")
        self.open = True
        self.update()

    def hide(self):
        """Close the popup."""
        self.open = False
        self.update()

    def updateinfo(self):
        """Run initialization logic when the popup is displayed."""
        if self.user_repo.user_id != 0:
            self.userid = self.user_repo.user_id
        self.fetch_reports()

    def fetch_reports(self):
        """Fetch all reports for the specific user and update self.reports."""
        try:
            # Clear the reports list to ensure no stale data
            self.reports.clear()

            # Query the database for reports connected to the specific user
            self.cursor.execute("SELECT report_id, report_type, report_date FROM reports WHERE user_id = ?", (self.userid,))
            rows = self.cursor.fetchall()

            # Populate the reports list with the fetched data
            for row in rows:
                report_id, report_type, report_date = row
                self.reports.append({
                    "report_id": report_id,
                    "report_type": report_type,
                    "report_date": report_date,
                })

            print("Updated Reports:", self.reports)

        except Exception as e:
            print(f"An error occurred while fetching reports: {e}")

    def refresh_reports(self, e, selected_month_year):
        """Refresh the reports table for a given month and year, printing transactions without time in the date."""
        print(f"Selected month-year: {selected_month_year}")

        if selected_month_year == "No data available":
            self.table.controls.clear()
            self.table.controls.append(
                ft.Text("No reports available for the selected month and year.", italic=True, color=self.colors.GREY_BACKGROUND, size=24)
            )
            self.table.update()
            return

        try:
            selected_month, selected_year = self.parse_month_year(selected_month_year)
            print(f"Selected month: {selected_month}, Selected year: {selected_year}")  # Debug output
        except ValueError as ve:
            print(f"Error parsing selected month-year: {ve}")
            self.table.controls.clear()
            self.table.controls.append(
                ft.Text("Invalid date format selected.", italic=True, color=self.colors.ERROR_RED, size=24)
            )
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
            self.table.controls.append(
                ft.Text("Invalid month selected.", italic=True, color=self.colors.ERROR_RED, size=24)
            )
            self.table.update()
            return

        selected_date_prefix = f"{selected_year}-{selected_month}"
        self.table.controls.clear()

        # Table Header
        self.table.controls.append(ft.Row([
            ft.Text("Account", weight="bold", width=200, color=self.colors.TEXT_COLOR, text_align="center", size=24),
            ft.Text("Balance", weight="bold", width=150, color=self.colors.TEXT_COLOR, text_align="center", size=24),
            ft.Text("Transactions", weight="bold", width=400, color=self.colors.TEXT_COLOR, text_align="center", size=24),
        ], alignment=ft.MainAxisAlignment.START, spacing=10))

        # Fetch JSON data and validate
        parsed_json_data = self.fetch_json_data()
        if not parsed_json_data:
            self.table.controls.append(
                ft.Text("No data found in reports.", italic=True, color=self.colors.GREY_BACKGROUND, size=24)
            )
            self.table.update()
            return

        for account in parsed_json_data:
            account_name = account["account_name"]
            balance = account["balance"]
            transactions = account["transactions"]

            # Filter transactions by selected month and year
            filtered_transactions = [
                transaction for transaction in transactions
                if transaction["date"].startswith(selected_date_prefix)
            ]

            # Account Row Header
            self.table.controls.append(
                ft.Row(
                    [
                        ft.Text(f"Account Name: {account_name}", width=200, color=self.colors.TEXT_COLOR, text_align="left", size=16),
                        ft.Text(f"Balance: ${balance:.2f}", width=150, color=self.colors.TEXT_COLOR, text_align="left", size=16),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                )
            )

            # Transaction Rows
            for transaction in filtered_transactions:
                description = transaction["description"]
                amount = transaction["amount"]
                date = transaction["date"].split()[0]  # Removes the time part, leaving only YYYY-MM-DD

                self.table.controls.append(
                    ft.Row(
                        [
                            ft.Text(description, width=200, text_align="left", size=16),
                            ft.Text(f"${amount:.2f}", width=150, text_align="left", size=16),
                            ft.Text(date, width=400, text_align="left", size=16),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                    )
                )

        # Refresh the table visually
        self.table.update()



    def fetch_json_data(self):
        """Fetch and parse JSON data from the reports table."""
        try:
            self.cursor.execute("SELECT report_data FROM reports WHERE user_id = ?", (self.userid,))
            result = self.cursor.fetchone()

            if result:
                json_data = json.loads(result[0])
                print("Parsed JSON Data:", json_data)
                return json_data
            else:
                print("No data found for the user.")
                return None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def parse_month_year(self, month_year):
        """Parse the combined month-year string and return month and year."""
        parts = month_year.split()
        if len(parts) != 2:
            raise ValueError("Invalid format")
        month, year = parts
        return month, year