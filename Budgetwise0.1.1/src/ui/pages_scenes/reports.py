import flet as ft
from datetime import datetime
import json

class Reports(ft.View):
    def __init__(self, page: ft.Page, user_data, NavRail, colors):
        super().__init__(route="/reports", bgcolor=colors.BLUE_BACKGROUND)

        self.page = page
        self.user_repo = user_data
        self.db = self.user_repo.db
        self.cursor = self.db.cursor()
        self.colors = colors

        self.userid = 1

        self.reports=[]

        # Title Row
        title_row = ft.Row(
            [
                ft.Text("Reports", size=30, weight="bold")
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=False,
        )

        # Reports Table Container
        self.reports_table = ft.Column(spacing=10, alignment=ft.MainAxisAlignment.CENTER)

        # Scrollable Wrapper for Table Content
        self.TableElements = ft.ListView(
            controls=[
                self.reports_table,  # Dynamic table elements
            ],
            expand=True,
            spacing=10,
        )

        # Wrap the Scrollable Container
        self.scrollable_table = ft.Container(
            content=self.TableElements,
            expand=True,
            padding=10,
        )

        # Refresh Button
        self.refresh_button = ft.Container(
            content=ft.ElevatedButton(
                text="Refresh Reports",
                on_click=self.refresh_reports,
            ),
            alignment=ft.alignment.bottom_center,  # Fixed at the bottom
            padding=10,
            expand=False,
        )

        # Main Content
        content = ft.Column(
            [
                title_row,
                # ----------------- PAGE CONTENT GOES BELOW -----------------
                self.scrollable_table,  # Scrollable table
                self.refresh_button,  # Fixed Refresh Button
                # ----------------- PAGE CONTENT GOES ABOVE -----------------
            ],
            expand=True,  # Make content expand to fill available space
        )

        self.controls = [
            ft.Row(
                [
                    NavRail.rail,  # Navigation bar
                    ft.VerticalDivider(width=1),  # Divider between navbar and content
                    content,
                ],
                expand=True,
            )
        ]
    def did_mount(self):
        # Refresh the dropdown each time the page is routed to
        if self.user_repo.user_id != 0:
            self.userid = self.user_repo.user_id
        self.fetch_reports()
        self.refresh_reports
    
    def fetch_reports(self):
        """Fetch all reports for the specific user and update self.reports."""
        try:
            # Clear the reports list to ensure no stale data

            # Query the database for reports connected to the specific user
            self.cursor.execute("SELECT report_id, report_type, report_date FROM reports WHERE user_id = ?", (self.userid,))
            rows = self.cursor.fetchall()

            # Populate the reports list with the fetched data
            for row in rows:
                report_id, report_type, report_date = row
                self.reports.append({
                    "report_id": report_id,
                    "report_type": report_type,
                    "report_date": report_date
                })

            # Debug print to verify the updated reports list
            print("Updated Reports:", self.reports)

        except Exception as e:
            print(f"An error occurred while fetching reports: {e}")

   

    def refresh_reports(self, e):
        # Clear existing table content
        self.reports_table.controls.clear()

        # Fetch the JSON data and store it
        parsed_json_data = self.fetch_json_data()  # Fetch JSON data (Parsed JSON Data)
        if not parsed_json_data:
            print("No parsed JSON data found.")
            return

        # Fetch the summary report data
        self.cursor.execute("SELECT report_id, report_type, report_date FROM reports WHERE user_id = ?", (self.userid,))
        rows = self.cursor.fetchall()

        # **Section 1: Updated Reports (Summary Table)**
        self.reports_table.controls.append(
            ft.Text("Updated Reports", size=20, weight="bold", color=self.colors.TEXT_COLOR)
        )

        self.reports_table.controls.append(
            ft.Row(
                [
                    ft.Text("ID", weight="bold", width=150, text_align="center", size=18),
                    ft.Text("Type", weight="bold", width=150, text_align="center", size=18),
                    ft.Text("Date", weight="bold", width=300, text_align="center", size=18),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            )
        )

        for row in rows:
            report_id, report_type, report_date = row
            self.reports_table.controls.append(
                ft.Row(
                    [
                        ft.Text(f"{report_id}", width=150, text_align="center", size=16),
                        ft.Text(f"{report_type}", width=150, text_align="center", size=16),
                        ft.Text(f"{report_date}", width=300, text_align="center", size=16),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                )
            )

        # **Section 2: Parsed JSON Data (Detailed Table with Transactions)**
        self.reports_table.controls.append(
            ft.Text("Parsed JSON Data", size=20, weight="bold", color=self.colors.TEXT_COLOR)
        )

        for account in parsed_json_data:
            account_name = account["account_name"]
            balance = account["balance"]
            transactions = account["transactions"]

            # Account Details Header Row
            self.reports_table.controls.append(
                ft.Row(
                    [
                        ft.Text(f"Account: {account_name}", size=18, weight="bold", width=300, text_align="center"),
                        ft.Text(f"Balance: ${balance:.2f}", size=18, width=300, text_align="center"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                )
            )

            # Transactions Header
            self.reports_table.controls.append(
                ft.Row(
                    [
                        ft.Text("Description", weight="bold", width=200, text_align="center", size=16),
                        ft.Text("Amount", weight="bold", width=150, text_align="center", size=16),
                        ft.Text("Date", weight="bold", width=300, text_align="center", size=16),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                )
            )

            # Transactions Rows
            for transaction in transactions:
                description = transaction["description"]
                amount = transaction["amount"]
                date = transaction["date"]

                self.reports_table.controls.append(
                    ft.Row(
                        [
                            ft.Text(description, width=200, text_align="center", size=14),
                            ft.Text(f"${amount:.2f}", width=150, text_align="center", size=14),
                            ft.Text(date, width=300, text_align="center", size=14),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    )
                )

        # Update the table to reflect changes
        self.page.update()
    
    def fetch_json_data(self):
        try:
            # Query to fetch JSON data from the database
            self.cursor.execute("SELECT report_data FROM reports WHERE report_id = ? AND user_id = ?", (1, self.userid, ))
            result = self.cursor.fetchone()

            if result:
                # Parse the JSON data
                json_data = json.loads(result[0])
                
                # Example: Access specific parts of the JSON data
                print("Parsed JSON Data:", json_data)
                # Example: Access a specific key-value pair
                if "key_name" in json_data:
                    print("Key Value:", json_data["key_name"])
                
                return json_data
            else:
                print("No data found for the given report_id.")
                return None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None