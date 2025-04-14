import flet as ft
from datetime import datetime
import json
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet

class Reports(ft.AlertDialog):
    def __init__(self, user_data, colors):
        super().__init__(modal=True)  # Initialize as an AlertDialog
        self.user_repo = user_data
        self.db = self.user_repo.db
        self.cursor = self.db.cursor()
        self.colors = colors

        self.month_name = 0
        self.year_name = 0
        self.month_year = 0
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
                on_click=lambda e: #self.generate_pdf_report(self.month_name, self.year_name)print
                                    print("Heh, I don't work... YET"),
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
        """Fetch all reports for the specific user, including report data, and update self.reports."""
        try:
            # Clear the reports list to ensure no stale data
            self.reports.clear()

            # Query the database for reports connected to the specific user, including report_data
            self.cursor.execute(
                "SELECT report_id, report_type, report_date, report_data FROM reports WHERE user_id = ?", 
                (self.userid,)
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


    def refresh_reports(self, e, selected_month_year):
        """Refresh the reports table for a given month and year, displaying accounts at the top and a centered transactions subtable."""
        print(f"Selected month-year: {selected_month_year}")

        if selected_month_year == "No data available":
            self.table.controls.clear()
            self.table.controls.append(
                ft.Text(
                    "No reports available for the selected month and year.", 
                    italic=True, color=self.colors.GREY_BACKGROUND, size=24
                )
            )
            self.table.update()
            return

        try:
            # Assume parse_month_year returns a tuple like (month_name, selected_year)
            month_name, selected_year = self.parse_month_year(selected_month_year)
            print(f"Selected month: {month_name}, Selected year: {selected_year}")
        except ValueError as ve:
            print(f"Error parsing selected month-year: {ve}")
            self.table.controls.clear()
            self.table.controls.append(
                ft.Text(
                    "Invalid date format selected.", italic=True, 
                    color=self.colors.ERROR_RED, size=24
                )
            )
            self.table.update()
            return

        # Convert month name to integer
        month_mapping = {
            "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
            "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
        }
        selected_month = month_mapping.get(month_name)
        if not selected_month:
            print(f"Invalid month selected: {month_name}")
            self.table.controls.clear()
            self.table.controls.append(
                ft.Text(
                    "Invalid month selected.", italic=True, 
                    color=self.colors.ERROR_RED, size=24
                )
            )
            self.table.update()
            return
        
        # Build the date prefix for filtering transactions (e.g., "2025-03")
        selected_date_prefix = f"{selected_year}-{selected_month:02d}"
        self.table.controls.clear()

        # Center the entire table contents
        self.table.alignment = ft.MainAxisAlignment.CENTER
        self.table.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Main table header (without a "Transactions" column now)
        self.table.controls.append(
            ft.Row(
                [
                    ft.Text("Account", weight="bold", width=200, text_align="center", size=24, color=self.colors.TEXT_COLOR),
                    ft.Text("Balance", weight="bold", width=150, text_align="center", size=24, color=self.colors.TEXT_COLOR),
                    ft.Text("Remaining", weight="bold", width=150, text_align="center", size=24, color=self.colors.TEXT_COLOR),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
        )

        # Fetch filtered JSON data
        self.month_name, self.year_name = selected_month, int(selected_year)
        parsed_json_data = self.fetch_json_data(e, (selected_month, int(selected_year)))
        if not parsed_json_data:
            self.table.controls.append(
                ft.Text("No data found in reports.", italic=True, color=self.colors.GREY_BACKGROUND, size=24)
            )
            self.table.update()
            return

        # Iterate over each report and over each account inside report_data
        for report in parsed_json_data:
            accounts = report.get("report_data", [])
            if not isinstance(accounts, list):
                accounts = [accounts]

            for account in accounts:
                account_name = account.get("account_name", "Unnamed Account")
                balance = account.get("balance", 0)
                transactions = account.get("transactions", [])

                # Filter transactions by the date prefix (YYYY-MM)
                filtered_transactions = [
                    transaction for transaction in transactions
                    if transaction["date"].startswith(selected_date_prefix)
                ]
                # Compute the remaining amount: balance minus the sum of transaction amounts
                total_transactions = sum(transaction.get("amount", 0) for transaction in filtered_transactions)
                computed_remaining = balance - total_transactions

                # Create the minor header row for transactions (for Description, Amount, Date)
                transaction_header_row = ft.Row(
                    [
                        ft.Text("Description", weight="bold", width=200, text_align="center", size=16, color=self.colors.TEXT_COLOR),
                        ft.Text("Amount", weight="bold", width=150, text_align="center", size=16, color=self.colors.TEXT_COLOR),
                        ft.Text("Date", weight="bold", width=150, text_align="center", size=16, color=self.colors.TEXT_COLOR)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                )

                # Build the transaction rows
                transaction_rows = [
                    ft.Row(
                        [
                            ft.Text(transaction.get("description", ""), width=200, text_align="center", size=16),
                            ft.Text(f"${transaction.get('amount', 0):.2f}", width=150, text_align="center", size=16),
                            ft.Text(transaction.get("date", "").split()[0], width=150, text_align="center", size=16)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10
                    )
                    for transaction in filtered_transactions
                ]

                # Create a subtable (transactions container) with the minor header and transaction rows.
                transactions_container = ft.Column(
                    controls=[
                        transaction_header_row,
                        *transaction_rows
                    ],
                    spacing=5,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )

                # Create a container for the account info and its transactions subtable
                account_container = ft.Container(
                    content=ft.Column(
                        controls=[
                            # Account header row with account name, balance, and computed remaining
                            ft.Row(
                                [
                                    ft.Text(f"Account Name: {account_name}", width=200, text_align="center", size=16, color=self.colors.TEXT_COLOR),
                                    ft.Text(f"Balance: ${balance:.2f}", width=150, text_align="center", size=16, color=self.colors.TEXT_COLOR),
                                    ft.Text(f"Remaining: ${computed_remaining:.2f}", width=150, text_align="center", size=16, color=self.colors.TEXT_COLOR),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=10
                            ),
                            ft.Divider(height=1, color=self.colors.GREY_BACKGROUND),
                            # Append the transactions container (which now has minor headers)
                            transactions_container
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    alignment=ft.alignment.center,
                    padding=10,
                    border=ft.border.all(1, self.colors.GREY_BACKGROUND)
                )

                # Add the centered account container to the main table view
                self.table.controls.append(account_container)

        # Finally, refresh the table visually
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



        
    def parse_month_year(self, month_year):
        """Parse the combined month-year string and return month and year."""
        parts = month_year.split()
        if len(parts) != 2:
            raise ValueError("Invalid format")
        month, year = parts
        return month, year
    
    # *this was doing something stupid, don't know if it works
    # def generate_pdf_report(self, month, year):
    #     """
    #     Generates a PDF report from the parsed JSON data using the data fetched from fetch_json_data.
    #     The PDF filename will be based on the passed month and year.
        
    #     :param month: Numeric month (e.g., 3 for March)
    #     :param year: Numeric year (e.g., 2025)
    #     """
    #     # Fetch the latest JSON data using the same arguments as in refresh_reports.
    #     parsed_json_data = self.fetch_json_data(None, (month, int(year)))
    #     if not parsed_json_data:
    #         print("No report data available.")
    #         return

    #     # Create a filename such as "Report_2025_03.pdf"
    #     filename = f"Report_{year}_{int(month):02d}.pdf"
    #     doc = SimpleDocTemplate(filename, pagesize=letter)
    #     elements = []

    #     # Get default styles
    #     styles = getSampleStyleSheet()
    #     title = Paragraph("Monthly Report", styles["Title"])
    #     elements.append(title)
    #     elements.append(Spacer(1, 12))

    #     # Iterate over each report and then over each account inside "report_data"
    #     for report in parsed_json_data:
    #         # Get the list of accounts from this report.
    #         accounts = report.get("report_data", [])
    #         if not isinstance(accounts, list):
    #             accounts = [accounts]
            
    #         for account in accounts:
    #             account_name = account.get("account_name", "Unnamed Account")
    #             balance = account.get("balance", 0)
    #             transactions = account.get("transactions", [])
    #             total_txn = sum(txn.get("amount", 0) for txn in transactions)
    #             remaining = account.get("remaining", balance - total_txn)
                
    #             # Build account header as a Paragraph
    #             account_header = Paragraph(
    #                 f"<b>Account:</b> {account_name}&nbsp;&nbsp;&nbsp; "
    #                 f"<b>Balance:</b> ${balance:.2f}&nbsp;&nbsp;&nbsp; "
    #                 f"<b>Remaining:</b> ${remaining:.2f}",
    #                 styles["Heading3"]
    #             )
    #             elements.append(account_header)
    #             elements.append(Spacer(1, 6))
                
    #             # Build the transaction table with headers
    #             table_data = [["Description", "Amount", "Date"]]
    #             for txn in transactions:
    #                 desc = txn.get("description", "")
    #                 amount = txn.get("amount", 0)
    #                 date = txn.get("date", "").split()[0]  # Remove time if needed
    #                 table_data.append([desc, f"${amount:.2f}", date])
                
    #             # Create the table with fixed column widths
    #             t = Table(table_data, colWidths=[200, 100, 100])
    #             t.setStyle(TableStyle([
    #                 ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    #                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    #                 ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    #                 ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    #                 ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    #                 ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    #                 ('GRID', (0, 0), (-1, -1), 1, colors.black),
    #             ]))
    #             elements.append(t)
    #             elements.append(Spacer(1, 12))

    #     # Build the PDF file
    #     doc.build(elements)
    #     print(f"PDF report generated and saved as {filename}")
