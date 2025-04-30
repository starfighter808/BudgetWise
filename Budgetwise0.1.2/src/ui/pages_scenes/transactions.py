import flet as ft
from datetime import datetime, timedelta


class Transactions(ft.View):
    def __init__(self, page: ft.Page, user_data, NavRail, colors, trans_funcs):
        super().__init__(route="/transactions", bgcolor=colors.GREY_BACKGROUND)
        self.debug_text = ft.Text("Debug output will appear here.", color="red")
        self.log_debug("Transactions page constructor started")
        # TODO: Store user_id AFTER user has logged in
        self.user_id = 1
        # self.user_id = self.user_data.get_user_id(self.user_data.username)

        # Retrieve budget ID for the user
        self.budget_id = 1

        self.controls.append(ft.Text("Transactions"))

        title_row = ft.Row(  # This is the title of the page
            [ft.Text("Transactions", size=30, weight="bold")],
            alignment=ft.MainAxisAlignment.CENTER,  # Center the title
            expand=False,  # Make the title row expand to fill available width
        )

        self.trans_funcs = trans_funcs
        self.returned_trans = []
        #this gets the userid's
        self.returned_trans = self.trans_funcs.getTransactionList(self.user_id)
        print(f"Raw transaction IDs: {self.returned_trans}")  # Debug raw data

        # Validate transaction details
        self.transDetails = []
        for TID in self.returned_trans:
            details = self.trans_funcs.getTransactionDetails(TID)
            print(f"TID {TID} details: {details}")  # Debug
            
            if not details or len(details) != 1:  # Check if the outer list has 1 item
                print(f"⚠️ Invalid details format for TID {TID}: {details}")
                continue
            
            transaction_data = details[0]  # Extract the inner tuple
            if len(transaction_data) != 7:  # Validate the tuple itself
                print(f"⚠️ Invalid transaction data for TID {TID}: {transaction_data}")
                continue
            
            self.transDetails.append(list(transaction_data))  # Convert tuple to list

            # details = self.trans_funcs.getTransactionDetails(TID)
            # print(f"TID {TID} returned: {details} (type: {type(details)})")
            # self.transDetails.append(list(details))
        #################################################
        # DEBUG SECTION
        #################################################
        # print("---- Transaction Details Dump ----")
        # for i, row in enumerate(self.transDetails):
        #     print(f"Row {i}: {row} (Length: {len(row)})")

        data_columns = [
            ft.DataColumn(ft.Text("Budget Account ID")),
            ft.DataColumn(ft.Text("Vendor ID")),
            ft.DataColumn(ft.Text("Transaction Type")),
            ft.DataColumn(ft.Text("Amount")),
            ft.DataColumn(ft.Text("Description")),
            ft.DataColumn(ft.Text("Recurring")),
            ft.DataColumn(ft.Text("Importance Rating")),
        ]

        data_rows = []
        try:
            for row_data in self.transDetails:
                # Ensure the row has the right number of columns (7)
                if len(row_data) != 7:
                    print(f"Skipping malformed row: {row_data}")
                    continue
                data_cells = [ft.DataCell(ft.Text(str(item))) for item in row_data]
                data_rows.append(ft.DataRow(cells=data_cells))
                if not data_rows:
                    data_rows.append(
                        ft.DataRow(cells=[ft.DataCell(ft.Text("No transactions found", color="red"))])
                    )
        except Exception as e:
            print("Error creating data rows:", e)


        self.table = ft.DataTable(
            columns=data_columns,
            rows=data_rows,
            expand=True,  # Make the table expand within its container
        )
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

        content = ft.Column(
            [
                title_row,
                # ----------------- PAGE CONTENT GOES BELOW -----------------
                self.scrollable_table,
                self.debug_text,
                # ----------------- PAGE CONTENT GOES ABOVE -----------------
            ],
            expand=True,  # Make content expand to take the remaining space
        )

        self.controls = [
            ft.Row(
                [
                    NavRail.rail,  # navigation bar
                    ft.VerticalDivider(
                        width=1
                    ),  # divider between navbar and page content
                    content,
                ],
                expand=True,
            )
        ]

    def log_debug(self, *messages):
        if not hasattr(self, 'debug_text') or not self.debug_text.page:
            print("[DEBUG]", *messages)  # Fallback to console
        else:
            self.debug_text.value = "\n".join(str(m) for m in messages)
            self.debug_text.update()
