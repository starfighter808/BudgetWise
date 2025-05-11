import flet as ft
from datetime import datetime
import json
from src.ui.pages_scenes.reports import Reports


class History(ft.View):
    def __init__(self, page: ft.Page,user_data, NavRail, colors):
        super().__init__(route="/history", bgcolor= colors.GREY_BACKGROUND)

        self.controls.append(ft.Text("History"))
        self.user_data = user_data
        self.colors = colors

        title_row = ft.Row( # This is the title of the page
        [
            ft.Text("History", size=30, weight="bold", color=self.colors.TEXT_COLOR)
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

        # combined_month_year_options = self.get_combined_month_year_options()
        # self.combined_dropdown = self.create_combined_month_year_dropdown(combined_month_year_options)
        reports_options = self.get_combined_report_options()
        self.report_dropdown=self.create_combined_report_dropdown(reports_options)

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
                self.report_dropdown,  # Dropdown for combined month-year
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
        self.refresh_report_dropdown(self.report_dropdown)
        self.reports_page.updateinfo()

    def refresh_report_dropdown(self, dropdown):
        """
        Refresh the dropdown to include unique identifiers for specific reports generated on the same day.
        """
        # Fetch all reports first
        self.fetch_reports()
        
        # Get combined options with identifiers
        combined_report_options = self.get_combined_report_options()
        
        # Handle case where no data is available
        if combined_report_options == ["No data available"]:
            dropdown.options = [ft.dropdown.Option("No options available")]
        else:
            dropdown.options = [ft.dropdown.Option(option) for option in combined_report_options]
        
        # Update the dropdown UI
        dropdown.update()

    def get_combined_report_options(self):
        """
        Extracts unique report options using the 'report_date' and an identifier (e.g., report ID or type).
        Returns a list of strings in the format "Month Day, Year - Identifier" (e.g., "March 25, 2025 - Report ID: 123").
        """
        if not self.reports:
            return ["No data available"]

        # Map month numbers to month names
        month_names = {
            '01': 'January', '02': 'February', '03': 'March', '04': 'April',
            '05': 'May', '06': 'June', '07': 'July', '08': 'August',
            '09': 'September', '10': 'October', '11': 'November', '12': 'December'
        }

        options = []
        for report in self.reports:
            report_date = report.get("report_date", "")
            report_id = report.get("report_id", "Unknown ID")  # Use report ID as an identifier
            if report_date:
                # Parse the full date format "YYYY-MM-DD"
                date_parts = report_date.split(" ")[0].split("-")
                if len(date_parts) == 3:
                    year, month, day = date_parts
                    month_name = month_names.get(month, month)
                    options.append(f"{month_name} {int(day)}, {year} - Report: {report_id}")
        
        # Return sorted options
        return sorted(options)

    def get_specific_report(self, selected_month_year, selected_report_id):
        """
        Retrieves a specific report for the given month/year and the report's unique identifier.
        """
        # Get all reports for the provided month and year.
        reports = self.fetch_json_data(None, selected_month_year)
        
        # Look for the report with the specific report_id.
        for report in reports:
            if report["report_id"] == selected_report_id:
                return report
        
        return None  # If no matching report is found.

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

        except Exception as e:
            print(f"An error occurred while fetching reports: {e}")

    def create_combined_report_dropdown(self, options):
        """
        Create a Dropdown with detailed options including date and report identifier.
        The dropdown has a dark gray background so that white text (when selected)
        is visible.
        """
        # Create your dropdown options.
        dropdown_options = [
            ft.dropdown.Option(opt, text_style=ft.TextStyle(color=ft.Colors.BLACK))
            for opt in self.get_combined_report_options()
        ]

        report_dropdown = ft.Dropdown(
            options=dropdown_options,
            width=200,
            text_style=ft.TextStyle(color=ft.Colors.WHITE),  # Selected text in white
            bgcolor=ft.Colors.BLACK,  # Set the background color of the dropdown
            on_change=lambda e: self.handle_dropdown_selection(e.data)
        )

        return report_dropdown



    def handle_dropdown_selection(self, selected_option):

        try:
            # Assume the string format is "Month Day, Year - Report: <report_id>"
            parts = selected_option.split(" - Report:")
            date_part = parts[0].strip()  # e.g., "April 10, 2025"
            # Convert date_part to a datetime object; we only need month and year for filtering
            dt = datetime.strptime(date_part, "%B %d, %Y")
            selected_month_year = (dt.month, dt.year)
            
            # Parse out the report ID
            selected_report_id = int(parts[1].strip())
        except Exception as ex:
            print(f"Error parsing selection: {ex}")
            return

        # Use the extracted information to retrieve the specific report.
        report = self.get_specific_report(selected_month_year, selected_report_id)
        
        if report:
            # Call both refresh functions using the same selected_option.
            # Note: If these functions require an event argument, you can pass None if not coming from an event.
            self.refresh_table()
            self.reports_page.refresh_reports(None, selected_option)



    
    def reports_button_clicked(self, e):
        """Handle the button click event and show the Reports popup."""
        self.reports_page.show() # Call the show() method of the Reports popup
        self.page.update()

    def refresh_table(self, e=None):
        """
        Refresh the table dynamically while maintaining its original structure and
        filling it with report data from JSON based on the specific report chosen from the dropdown.
        Additionally, for each transaction, if its date is after the report's creation date,
        mark it with a "Scheduled" tag and DO NOT include it in the balance calculation.
        """
        # Obtain the full selected option string from the dropdown.
        selected_option = self.report_dropdown.value

        if selected_option == "No data available":
            self.table.controls.clear()
            self.table.controls.append(
                ft.Text("No reports available for the selected month and year.",
                        italic=True, color=self.colors.GREY_BACKGROUND, size=24)
            )
            self.table.update()
            return

        # Parse the dropdown option.
        # Expected format: "April 10, 2025 - Report: 4"
        try:
            parts = selected_option.split(" - Report:")
            date_part = parts[0].strip()          # e.g., "April 10, 2025"
            report_id_str = parts[1].strip()        # e.g., "4"
            selected_report_id = int(report_id_str)

            # Use datetime.strptime to extract the month and year.
            dt = datetime.strptime(date_part, "%B %d, %Y")
            selected_month_year = (dt.month, dt.year)
        except Exception as ex:
            print(f"Error parsing selected option: {ex}")
            self.table.controls.clear()
            self.table.controls.append(
                ft.Text("Invalid selection format.",
                        italic=True, color=self.colors.ERROR_RED, size=24)
            )
            self.table.update()
            return

        # Retrieve the specific report.
        report = self.get_specific_report(selected_month_year, selected_report_id)
        if not report:
            self.table.controls.clear()
            self.table.controls.append(
                ft.Text("No report data found for the selected option.",
                        italic=True, color=self.colors.GREY_BACKGROUND, size=24)
            )
            self.table.update()
            return

        # Get the accounts data from the report.
        accounts = report.get("report_data", [])
        if not isinstance(accounts, list):
            accounts = [accounts]

        # Clear the current table controls.
        self.table.controls.clear()

        # Table Header Row.
        self.table.controls.append(ft.Row([
            ft.Text("Account", weight="bold", width=200, color=self.colors.BLUE_BACKGROUND, text_align="center", size=24),
            ft.Text("Balance", weight="bold", width=150, color=self.colors.BLUE_BACKGROUND, text_align="center", size=24),
            ft.Text("Allocation", weight="bold", width=300, color=self.colors.BLUE_BACKGROUND, text_align="center", size=24),
            ft.Text("Transactions", weight="bold", width=300, color=self.colors.BLUE_BACKGROUND, text_align="center", size=24),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10))

        # Get the report creation date.
        report_creation_dt = report.get("report_date")
        if isinstance(report_creation_dt, str):
            try:
                report_creation_dt = datetime.strptime(report_creation_dt, "%Y-%m-%d %H:%M:%S")
            except Exception as ex:
                print(f"Error converting report creation date: {ex}")
                report_creation_dt = None

        # Iterate over each account.
        for account in accounts:
            account_name = account.get("account_name", "Unnamed Account")
            balance = account.get("balance", 0)
            transactions = account.get("transactions", [])

            total_spent = 0  # This will only accumulate amounts from non-scheduled (completed) transactions.
            display_transactions = []  # Holds transactions along with their status.

            # Process each transaction.
            for transaction in transactions:
                # Assume transaction date is formatted as "YYYY-MM-DD" (or similar).
                txn_date = datetime.strptime(transaction["date"].split()[0], "%Y-%m-%d")
                # If the transaction date is after the report creation date, mark it as scheduled.
                if report_creation_dt and txn_date.date() > report_creation_dt.date():
                    status = "Scheduled"
                else:
                    status = ""
                    total_spent += transaction.get("amount", 0)
                display_transactions.append(
                    (
                        transaction.get("description", ""),
                        transaction.get("amount", 0),
                        transaction.get("date", ""),
                        status
                    )
                )

            updated_balance = balance - total_spent

            # Instead of a standard progress bar, use the custom meter widget.
            custom_meter = self.create_custom_meter(balance, updated_balance, width=300, height=10)

            # Build the sub-table header row with an extra "Status" column.
            sub_table_header = ft.Row(
                controls=[
                    ft.Text("Description", weight="bold", width=200, color=self.colors.GREEN_BUTTON, text_align="center", size=18),
                    ft.Text("Amount", weight="bold", width=150, color=self.colors.GREEN_BUTTON, text_align="center", size=18),
                    ft.Text("Transaction Date", weight="bold", width=150, color=self.colors.GREEN_BUTTON, text_align="center", size=18),
                    ft.Text("Status", weight="bold", width=100, color=self.colors.GREEN_BUTTON, text_align="center", size=18),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )

            # Build sub-table rows for each transaction.
            sub_table_rows = ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(desc, width=200, color=self.colors.TEXT_COLOR, text_align="center", size=16),
                            ft.Text(f"${amount:.2f}", width=150, color=self.colors.TEXT_COLOR, text_align="center", size=16),
                            ft.Text(date, width=150, color=self.colors.TEXT_COLOR, text_align="center", size=16),
                            ft.Text(
                                status,
                                width=100,
                                text_align="center",
                                size=16,
                                color=self.colors.BLUE_BACKGROUND if status == "Scheduled" else self.colors.TEXT_COLOR,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ) for desc, amount, date, status in display_transactions
                ]
            )

            # Create the sub-table container (hidden by default).
            sub_table = ft.Container(
                content=ft.Column([sub_table_header, sub_table_rows]),
                visible=False,
                padding=10,
            )

            # Toggle button to show/hide the sub-table.
            toggle_button = ft.ElevatedButton(
                text="View Transactions",
                on_click=lambda e, container=sub_table: self.toggle_sub_table(container),
                width=150
            )

            # Assemble the account row, with the custom meter in place of the standard progress bar.
            self.table.controls.append(ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(account_name, width=200, color=self.colors.TEXT_COLOR, text_align="center", size=16),
                        ft.Text(f"${updated_balance:.2f}", width=150, color=self.colors.TEXT_COLOR, text_align="center", size=16),
                        ft.Container(content=custom_meter, alignment=ft.alignment.center, width=300),
                        ft.Container(content=toggle_button, alignment=ft.alignment.center, width=300),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    sub_table
                ]),
                padding=10
            ))

        # Finally, update the table display.
        self.table.update()




    def create_custom_meter(self, allocated_balance, current_balance, width=300, height=10):
        """
        Returns a custom meter widget showing the allocated amount.
        
        - When current_balance is positive, the green portion fills rightward.
        - When current_balance is negative (overspent), a red bar extends to the left.
        """
        # Compute ratios based on the allocated (total) balance.
        if current_balance >= 0:
            positive_ratio = min(current_balance / allocated_balance, 1.0)
            negative_ratio = 0
        else:
            positive_ratio = 0
            negative_ratio = min(abs(current_balance) / allocated_balance, 1.0)

        # Base container represents the full allocated balance.
        base_container = ft.Container(
            width=width,
            height=height,
            bgcolor=ft.Colors.GREY_300,
            border_radius=5,
        )

        # Green container will fill from the left for positive funds.
        positive_container = ft.Container(
            width=width * positive_ratio,
            height=height,
            bgcolor=ft.Colors.GREEN,
            border_radius=5,
            alignment=ft.alignment.center_left,
        )

        # Red container represents overspending (drawn to the left).
        negative_container = ft.Container(
            width=width * negative_ratio,
            height=height,
            bgcolor=ft.Colors.RED,
            border_radius=5,
            alignment=ft.alignment.center_right,
        )

        # Use a Stack to overlay the containers.
        meter = ft.Stack(
            controls=[
                base_container,
                positive_container,
                negative_container,
            ]
        )
        return meter





    def fetch_json_data(self, e, selected_month_year, selected_report_id=None):
        """
        Filter the list self.reports for reports from the specified month and year,
        parse their JSON 'report_data', and return a list of dictionaries formatted for display.
        If selected_report_id is provided, only include the report with that ID.
        """
        month, year = selected_month_year
        parsed_reports = []

        for report in self.reports:
            try:
                # Assumes the format is 'YYYY-MM-DD HH:MM:SS'
                report_date_obj = datetime.strptime(report["report_date"], "%Y-%m-%d %H:%M:%S")
            except Exception as ex:
                print(f"Error parsing date for report_id {report['report_id']}: {ex}")
                continue

            if report_date_obj.month == month and report_date_obj.year == year:
                # If a specific report ID was provided, filter out non-matching reports
                if selected_report_id is not None and report["report_id"] != selected_report_id:
                    continue

                try:
                    parsed_data = json.loads(report["report_data"])
                except Exception as ex:
                    print(f"Error parsing JSON for report_id {report['report_id']}: {ex}")
                    parsed_data = None

                parsed_reports.append({
                    "report_id": report["report_id"],
                    "report_type": report["report_type"],
                    "report_date": report_date_obj,
                    "report_data": parsed_data  # Contains your account data
                })
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
