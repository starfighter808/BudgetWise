import flet as ft
from datetime import datetime
import json
import tkinter as tk
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
class Reports(ft.AlertDialog):
    def __init__(self, user_data, colors):
        super().__init__(modal=True)  # Initialize as an AlertDialog
        self.user_repo = user_data
        self.db = self.user_repo.db
        self.cursor = self.db.cursor()
        self.colors = colors

        self.month_name = 0
        self.year_name = 0
        self.report_id = 0
        self.month_year = 0
        self.userid = 1
        self.reports = []

        # Title Row
        title_row = ft.Row(
            [ft.Text("Reports", size=30, weight="bold", color=self.colors.TEXT_COLOR)],
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
                on_click=lambda e: self.generate_pdf_report(self.month_name, self.year_name, self.report_id),
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
            bgcolor=self.colors.GREY_BACKGROUND,
            expand=True,
            width=960,
            height=960  # Set the desired width (e.g., 800 pixels)
        )


    def show(self):
        """Show the popup."""
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

        except Exception as e:
            print(f"An error occurred while fetching reports: {e}")

    def refresh_reports(self, e, selected_option):
        """
        Refresh the reports table for a specific report.
        The selected_option is expected to be in the format "Month Day, Year - Report: <report_id>".
        In this version:
        - All transactions for each account are shown (no filtering by date prefix).
        - For each transaction, if its date is after the report creation date, a "Scheduled" tag is shown in the Status column.
        """

        if selected_option == "No data available":
            self.table.controls.clear()
            self.table.controls.append(
                ft.Text(
                    "No reports available for the selected option.",
                    italic=True, color=self.colors.GREY_BACKGROUND, size=24
                )
            )
            self.table.update()
            return

        # Parse the selected option into a date and report ID.
        try:
            # Expecting a format like "April 10, 2025 - Report: 4"
            parts = selected_option.split(" - Report:")
            date_part = parts[0].strip()         # e.g., "April 10, 2025"
            report_id_str = parts[1].strip()       # e.g., "4"
            selected_report_id = int(report_id_str)

            # Parse the date part to get month and year.
            dt = datetime.strptime(date_part, "%B %d, %Y")
            self.month_name, self.year_name = dt.month, dt.year
            selected_month_year = (dt.month, dt.year)
        except Exception as ex:
            print(f"Error parsing selection: {ex}")
            self.table.controls.clear()
            self.table.controls.append(
                ft.Text(
                    "Invalid selection format.",
                    italic=True, color=self.colors.ERROR_RED, size=24
                )
            )
            self.table.update()
            return

        # Retrieve the specific report using fetch_json_data.
        self.report_id = selected_report_id
        reports = self.fetch_json_data(e, selected_month_year, selected_report_id)
        if not reports:
            self.table.controls.clear()
            self.table.controls.append(
                ft.Text(
                    "No report data found for the selected option.",
                    italic=True, color=self.colors.GREY_BACKGROUND, size=24
                )
            )
            self.table.update()
            return

        # Since we filtered by report_id, we expect at most one report.
        report = reports[0]

        # Get the accounts data from the report.
        accounts = report.get("report_data", [])
        if not isinstance(accounts, list):
            accounts = [accounts]

        # Clear current table controls and set table alignment.
        self.table.controls.clear()
        self.table.alignment = ft.MainAxisAlignment.CENTER
        self.table.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Build the table header (Account, Balance, Remaining).
        self.table.controls.append(
            ft.Row(
                [
                    ft.Text("Account", weight="bold", width=200, text_align="center", size=24, color=self.colors.BLUE_BACKGROUND),
                    ft.Text("Balance", weight="bold", width=150, text_align="center", size=24, color=self.colors.BLUE_BACKGROUND),
                    ft.Text("Remaining", weight="bold", width=150, text_align="center", size=24, color=self.colors.BLUE_BACKGROUND),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
        )

        # Get the report creation date and ensure it is a datetime object.
        report_creation_dt = report.get("report_date")
        if isinstance(report_creation_dt, str):
            try:
                report_creation_dt = datetime.strptime(report_creation_dt, "%Y-%m-%d %H:%M:%S")
            except Exception as e:
                print(f"Error converting report creation date: {e}")
                report_creation_dt = None

        # Loop through each account in the report.
        for account in accounts:
            account_name = account.get("account_name", "Unnamed Account")
            balance = account.get("balance", 0)
            transactions = account.get("transactions", [])

            # Use all transactions (removing the previous date prefix filter).
            all_transactions = transactions
            total_transactions = sum(transaction.get("amount", 0) for transaction in all_transactions)
            computed_remaining = balance - total_transactions

            # Build header for the transactions sub-table with a Status column.
            transaction_header_row = ft.Row(
                controls=[
                    ft.Text("Description", weight="bold", width=200, text_align="center", size=16, color = self.colors.GREEN_BUTTON),
                    ft.Text("Amount", weight="bold", width=150, text_align="center", size=16, color = self.colors.GREEN_BUTTON),
                    ft.Text("Date", weight="bold", width=150, text_align="center", size=16, color = self.colors.GREEN_BUTTON),
                    ft.Text("Status", weight="bold", width=100, text_align="center", size=16, color = self.colors.GREEN_BUTTON),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )

            # Build rows for each transaction.
            transaction_rows = [
                ft.Row(
                    controls=[
                        ft.Text(transaction.get("description", ""), width=200,  color = self.colors.TEXT_COLOR, text_align="center", size=16),
                        ft.Text(f"${transaction.get('amount', 0):.2f}", width=150,  color = self.colors.TEXT_COLOR, text_align="center", size=16),
                        ft.Text(transaction.get("date", "").split()[0], width=150,  color = self.colors.TEXT_COLOR, text_align="center", size=16),
                        (
                            lambda t_date: ft.Text(
                                "Scheduled",
                                width=100,
                                text_align="center",
                                size=16,
                                color=self.colors.BLUE_BACKGROUND
                            ) if t_date and report_creation_dt and t_date.date() > report_creation_dt.date()
                            else ft.Text("", width=100)
                        )(datetime.strptime(transaction["date"].split()[0], "%Y-%m-%d"))
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                )
                for transaction in all_transactions
            ]

            transactions_container = ft.Column(
                controls=[transaction_header_row] + transaction_rows,
                spacing=5,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )

            # Build the account container.
            account_container = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            [
                                ft.Text(f"Account Name: {account_name}", width=200, text_align="center", size=16, color=self.colors.TEXT_COLOR),
                                ft.Text(f"Balance: ${balance:.2f}", width=150, text_align="center", size=16, color=self.colors.TEXT_COLOR),
                                ft.Text(f"Remaining: ${computed_remaining:.2f}", width=150, text_align="center", size=16, color=self.colors.TEXT_COLOR)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10
                        ),
                        ft.Divider(height=1, color=self.colors.GREY_BACKGROUND),
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
            self.table.controls.append(account_container)

        # Finally, update the table display.
        self.table.update()





    def fetch_json_data(self, e, selected_month_year, selected_report_id=None):
        """
        Filter the list self.reports for reports from the specified month and year,
        parse their JSON 'report_data', and return a list of dictionaries formatted for display.
        If selected_report_id is provided, only include the report with that ID.
        """
        # Unpack the tuple; expect selected_month_year to be like (3, 2025)
        month, year = selected_month_year
        parsed_reports = []

        for report in self.reports:
            try:
                # Assumes the format is 'YYYY-MM-DD HH:MM:SS'
                report_date_obj = datetime.strptime(report["report_date"], "%Y-%m-%d %H:%M:%S")

            except Exception as ex:
                print(f"Error parsing date for report_id {report['report_id']}: {ex}")
                continue

            # Only include reports with matching month and year
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
                    "report_data": parsed_data  # This contains your account data
                })
        return parsed_reports




        
    def parse_month_year(self, month_year):
        """Parse the combined month-year string and return month and year."""
        parts = month_year.split()
        if len(parts) != 2:
            raise ValueError("Invalid format")
        month, year = parts
        return month, year
    
    # *this was doing something stupid, don't know if it work

    def generate_pdf_report(self, month, year, selected_report_id):
        """
        Generates a PDF report from the parsed JSON data for a specific report 
        (identified by selected_report_id). It brings up a "Save As" dialog so
        the user can choose where to save the PDF.
        
        :param month: Numeric month (e.g., 3 for March)
        :param year: Numeric year (e.g., 2025)
        :param selected_report_id: The unique report ID that uniquely identifies the report selected.
        """
        # Fetch the specific report using fetch_json_data. (This function is assumed 
        # to accept an optional last parameter, filtering by report_id.)
        parsed_json_data = self.fetch_json_data(None, (int(month), int(year)), selected_report_id)
        if not parsed_json_data:
            return

        # Since we filtered by report_id, we expect exactly one report.
        report = parsed_json_data[0]

        # Bring up a "Save As" dialog.
        root = tk.Tk()
        root.withdraw()  # Hide the root window.
        # Prefix the default filename.
        default_filename = f"Report_{year}_{int(month):02d}.pdf"
        file_path = filedialog.asksaveasfilename(
            title="Save Report As",
            initialfile=default_filename,
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        # If the user cancelled the dialog, file_path will be an empty string.
        if not file_path:
            return

        # Create the PDF document using ReportLab.
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        elements = []

        # Get default styles.
        styles = getSampleStyleSheet()
        title = Paragraph("Monthly Report", styles["Title"])
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Iterate over the accounts in the report.
        accounts = report.get("report_data", [])
        if not isinstance(accounts, list):
            accounts = [accounts]
        
        for account in accounts:
            account_name = account.get("account_name", "Unnamed Account")
            balance = account.get("balance", 0)
            transactions = account.get("transactions", [])
            total_txn = sum(txn.get("amount", 0) for txn in transactions)
            remaining = balance - total_txn

            # Build account header as a Paragraph.
            account_header = Paragraph(
                f"<b>Account:</b> {account_name}&nbsp;&nbsp;&nbsp; "
                f"<b>Balance:</b> ${balance:.2f}&nbsp;&nbsp;&nbsp; "
                f"<b>Remaining:</b> ${remaining:.2f}",
                styles["Heading3"]
            )
            elements.append(account_header)
            elements.append(Spacer(1, 6))
            
            # Build the transaction table with headers.
            table_data = [["Description", "Amount", "Date"]]
            for txn in transactions:
                desc = txn.get("description", "")
                amount = txn.get("amount", 0)
                date = txn.get("date", "").split()[0]  # Removing time if present.
                table_data.append([desc, f"${amount:.2f}", date])
            
            # Create the table with fixed column widths.
            t = Table(table_data, colWidths=[200, 100, 100])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 12))

        # Build the PDF file.
        doc.build(elements)
        print(f"PDF report generated and saved as {file_path}")

