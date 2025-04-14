import flet as ft
from datetime import datetime
import json
from src.ui.pages_scenes.reports import Reports


class History(ft.View):
    def __init__(self, page: ft.Page,user_data, NavRail, colors):
        super().__init__(route="/history", bgcolor= colors.BLUE_BACKGROUND)

        self.controls.append(ft.Text("History"))
        self.user_data = user_data
        self.colors = colors

        title_row = ft.Row( # This is the title of the page
        [
            ft.Text("History", size=30, weight="bold")
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=False,
        )
        self.page = page
        self.user_data =user_data
        self.user_id = self.user_data.user_id
        
        # Use the existing database connection fromuser_data
        self.db = self.user_data.db
        self.cursor = self.db.cursor()

        # Retrieve budget ID for the user
        self.budget_id = self.user_data.budget_id
        self.reports = []

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

        combined_month_year_options = self.get_combined_month_year_options()
        self.combined_dropdown = self.create_combined_month_year_dropdown(combined_month_year_options)
        self.combined_dropdown.on_change = self.refresh_table

        self.reports_page = Reports(user_data, colors)
        self.page.overlay.append(self.reports_page)
        self.reports_button = ft.Container(
            content=ft.ElevatedButton(
                text="Reports",
                on_click=self.reports_button_clicked,
            ),
            alignment=ft.alignment.bottom_center,  # Position at the bottom center
            padding=10,
            expand=False,
        )
        content = ft.Column(
            [
                title_row,
                self.combined_dropdown,  # Dropdown for combined month-year
                # ----------------- PAGE CONTENT GOES BELOW -----------------
                self.scrollable_table,
                self.reports_button
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
        if self.user_data.user_id != 0:
            self.user_id = self.user_data.user_id
        self.refresh_combined_month_year_dropdown(self.combined_dropdown)
        self.reports_page.updateinfo()

    def refresh_combined_month_year_dropdown(self, dropdown):
        # Get combined month-year options
        self.fetch_reports()
        combined_month_year_options = self.get_combined_month_year_options()
        
        # Handle case where no data is available
        if combined_month_year_options == ["No data available"]:
            dropdown.options = [ft.dropdown.Option("No options available")]
        else:
            dropdown.options = [ft.dropdown.Option(option) for option in combined_month_year_options]
        
        # Update the dropdown UI
        dropdown.update()

    def get_combined_month_year_options(self):
        """
        Extracts distinct month-year options from self.reports using the 'report_date' key.
        Returns a list of strings in the format "Month Year" (e.g. "March 2025").
        """
        if not self.reports:
            return ["No data available"]
        
        # Collect distinct year-month strings (formatted as "YYYY-MM")
        distinct_ym = set()
        for report in self.reports:
            report_date = report.get("report_date", "")
            if report_date:
                # Assuming report_date is in format "YYYY-MM-DD ..." or similar,
                # we extract the first 7 characters to get "YYYY-MM"
                ym = report_date.split(" ")[0][:7]
                distinct_ym.add(ym)
        
        # Sort the year-month strings (sorting works lexicographically for "YYYY-MM")
        sorted_ym = sorted(distinct_ym)
        
        # Map month numbers to month names
        month_names = {
            '01': 'January', '02': 'February', '03': 'March', '04': 'April', 
            '05': 'May', '06': 'June', '07': 'July', '08': 'August', 
            '09': 'September', '10': 'October', '11': 'November', '12': 'December'
        }
        
        # Convert "YYYY-MM" into "Month Year" format
        options = []
        for ym in sorted_ym:
            year, month = ym.split("-")
            month_name = month_names.get(month, month)
            options.append(f"{month_name} {year}")
        
        return options

    def fetch_reports(self):
        """Fetch all reports for the specific user, including report data, and update self.reports."""
        try:
            # Clear the reports list to ensure no stale data
            self.reports.clear()

            # Query the database for reports connected to the specific user, including report_data
            self.cursor.execute(
                "SELECT report_id, report_type, report_date, report_data FROM reports WHERE user_id = ?", 
                (self.user_id,)
            )
            rows = self.cursor.fetchall()

            # Populate the reports list with the fetched data
            for row in rows:
                report_id, report_type, report_date, report_data = row
                self.reports.append({
                    "report_id": report_id,
                    "report_type": report_type,
                    "report_date": report_date,
                    "report_data": report_data,  # Include report_data
                })

            print("Updated Reports with Data:", self.reports)

        except Exception as e:
            print(f"An error occurred while fetching reports: {e}")

    
    def create_combined_month_year_dropdown(self, options):
        # Create Dropdown
        combined_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(option) for option in options],
            width=200,
            #height=50,
            on_change=lambda e: print(f"Selected {e.control.value}")
        )
        return combined_dropdown
    
    def reports_button_clicked(self, e):
        """Handle the button click event and show the Reports popup."""
        print("Show activated")
        self.reports_page.show() # Call the show() method of the Reports popup
        self.page.update()

        
    def refresh_table(self, e=None):
        """Refresh the table dynamically while maintaining its original structure and filling it with report data from JSON."""
        selected_month_year = self.combined_dropdown.value
        print(f"Selected month-year: {selected_month_year}")
        

        if selected_month_year == "No data available":
            self.table.controls.clear()
            self.table.controls.append(
                ft.Text("No reports available for the selected month and year.", italic=True, color=self.colors.GREY_BACKGROUND, size=24)
            )
            self.table.update()
            return
        self.reports_page.refresh_reports(e, selected_month_year)
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
            'January': 1, 'February': 2, 'March': 3, 'April': 4,
            'May': 5, 'June': 6, 'July': 7, 'August': 8,
            'September': 9, 'October': 10, 'November': 11, 'December': 12
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

        selected_date_prefix = f"{selected_year}-{selected_month:02d}"
        self.table.controls.clear()

        # Table Header
        self.table.controls.append(ft.Row([
            ft.Text("Account", weight="bold", width=200, color=self.colors.TEXT_COLOR, text_align="center", size=24),
            ft.Text("Balance", weight="bold", width=150, color=self.colors.TEXT_COLOR, text_align="center", size=24),
            ft.Text("Allocation", weight="bold", width=300, color=self.colors.TEXT_COLOR, text_align="center", size=24),
            ft.Text("Transactions", weight="bold", width=300, color=self.colors.TEXT_COLOR, text_align="center", size=24),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10))

        # Fetch JSON data and validate
        parsed_json_data = self.fetch_json_data(e, (selected_month, int(selected_year)))
        if not parsed_json_data:
            self.table.controls.append(
                ft.Text("No data found in reports.", italic=True, color=self.colors.GREY_BACKGROUND, size=24)
            )
            self.table.update()
            return
        for report in parsed_json_data:
            accounts = report.get("report_data", [])
            if not isinstance(accounts, list):
                accounts = [accounts]
            for account in accounts:
                account_name = account["account_name"]
                balance = account["balance"]
                transactions = account["transactions"]

                # Filter transactions by selected month and year
                filtered_transactions = [
                    transaction for transaction in transactions
                    if transaction["date"].startswith(selected_date_prefix)
                ]

                recent_transactions = filtered_transactions[:10]
                total_spent = sum(transaction["amount"] for transaction in filtered_transactions)
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
                                ft.Text(transaction["description"], width=200, text_align="center", size=16),
                                ft.Text(f"${transaction['amount']:.2f}", width=150, text_align="center", size=16),
                                ft.Text(transaction["date"], width=200, text_align="center", size=16),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ) for transaction in recent_transactions
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

        # Refresh the table visually
        self.table.update()



    def fetch_json_data(self, e, selected_month_year):
        """
        Filter the list self.reports for reports from the specified month and year,
        parse their JSON 'report_data', and return a list of dictionaries formatted for display.
        """
        # Unpack the tuple; expect selected_month_year to be like (3, 2025)
        month, year = selected_month_year
        parsed_reports = []

        for report in self.reports:
            try:
                # Assumes the format is 'YYYY-MM-DD HH:MM:SS'
                report_date_obj = datetime.strptime(report["report_date"], "%Y-%m-%d %H:%M:%S")
                # Debug: print the report's month/year
                print(f"Report ID {report['report_id']} date: {report_date_obj.month}/{report_date_obj.year}")
            except Exception as ex:
                print(f"Error parsing date for report_id {report['report_id']}: {ex}")
                continue

            # Only include reports with matching month and year
            if report_date_obj.month == month and report_date_obj.year == year:
                try:
                    parsed_data = json.loads(report["report_data"])
                except Exception as ex:
                    print(f"Error parsing JSON for report_id {report['report_id']}: {ex}")
                    parsed_data = None

                parsed_reports.append({
                    "report_id": report["report_id"],
                    "report_type": report["report_type"],
                    "report_date": report_date_obj,
                    "report_data": parsed_data  # This contains your account data
                })

        print("Parsed reports ready for display:", parsed_reports)
        return parsed_reports

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
