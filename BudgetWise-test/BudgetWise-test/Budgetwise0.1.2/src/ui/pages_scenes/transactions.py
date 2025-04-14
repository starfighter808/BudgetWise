import flet as ft
from datetime import datetime, timedelta


class Transactions(ft.View):
    def __init__(self, page: ft.Page, user_data, NavRail, colors, trans_funcs):
        super().__init__(route="/transactions", bgcolor=colors.BLUE_BACKGROUND)

        # TODO: Store userid AFTER user has logged in
        self.userid = 1
        # self.userid = self.user_data.get_user_id(self.user_data.username)

        # Retrieve budget ID for the user
        self.budgetid = 1

        self.controls.append(ft.Text("Transactions"))

        title_row = ft.Row(  # This is the title of the page
            [ft.Text("Transactions", size=30, weight="bold")],
            alignment=ft.MainAxisAlignment.CENTER,  # Center the title
            expand=False,  # Make the title row expand to fill available width
        )

        # gather transaction ID's
        self.trans_funcs = trans_funcs
        returned_trans = self.trans_funcs.getTransactionList(self.userid)
        self.transDetails = []
        # This loop should append the transaction details of all transactions to the list self.transDetails (2D list)
        for TID in returned_trans:
            self.transDetails.append(list(self.trans_funcs.getTransactionDetails(TID)))

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
        for row_data in self.transDetails:
            data_cells = [ft.DataCell(ft.Text(str(item))) for item in row_data]
            data_rows.append(ft.DataRow(cells=data_cells))

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
