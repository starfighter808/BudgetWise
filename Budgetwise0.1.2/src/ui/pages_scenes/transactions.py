import flet as ft
from src.ui.components.add_vendor import AddVendor
from src.ui.components.add_transaction import AddTransaction

class Transactions(ft.View):
    def __init__(self, page: ft.Page, user_data, NavRail, colors, trans_funcs, vend_funcs):
        super().__init__(route="/transactions", bgcolor=colors.GREY_BACKGROUND)
        print("Transactions page constructor started")

        self.page = page
        self.user_data = user_data
        self.user_id = self.user_data.user_id
        self.budget_id = self.user_data.budget_id
        self.vend_funcs = vend_funcs
        self.trans_funcs = trans_funcs
        self.returned_trans = []

        # Dialogs
        self.add_vendor_dialog = AddVendor(user_data, colors, vend_funcs)
        self.add_vendor_dialog.refresh = self.refresh_after_vendor_add
        self.page.overlay.append(self.add_vendor_dialog)

        self.add_transaction_dialog = AddTransaction(page, user_data, colors, trans_funcs, vend_funcs)
        self.add_transaction_dialog.refresh = self.refresh_after_transaction_add
        self.page.overlay.append(self.add_transaction_dialog)

        # UI Components
        title_row = ft.Row(
            [ft.Text("Transactions", size=30, weight="bold")],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=False,
        )

        self.add_vendor_button = ft.ElevatedButton("Add Vendor", on_click=self.show_add_vendor_dialog)
        self.add_transaction_button = ft.ElevatedButton("Add Transaction", on_click=self.show_add_transaction_dialog)

        self.transDetails = []
        self.returned_trans = self.trans_funcs.getTransactionList(self.user_id)
        self.prepare_transaction_details()

        data_columns = [
            ft.DataColumn(ft.Text("Transaction ID")),
            ft.DataColumn(ft.Text("Budget Account Name")),
            ft.DataColumn(ft.Text("Amount")),
            ft.DataColumn(ft.Text("Description")),
            ft.DataColumn(ft.Text("Recurring")),
            ft.DataColumn(ft.Text("Actions")),
        ]

        data_rows = self.create_transaction_rows()

        if not data_rows:
            data_rows = [
                ft.DataRow(cells=[ft.DataCell(ft.Text("No transactions found", color="red"))] +
                           [ft.DataCell(ft.Text("")) for _ in range(5)])
            ]

        self.table = ft.DataTable(columns=data_columns, rows=data_rows, expand=True)
        self.TableElements = ft.ListView(controls=[self.table], expand=True, spacing=10)
        self.scrollable_table = ft.Container(content=self.TableElements, expand=True, padding=10)

        content = ft.Column(
            [
                title_row,
                self.scrollable_table,
                self.add_vendor_button,
                self.add_transaction_button,
            ],
            expand=True,
        )

        self.controls = [
            ft.Row(
                [
                    NavRail.rail,
                    ft.VerticalDivider(width=1),
                    content,
                ],
                expand=True,
            )
        ]

    def refresh_after_transaction_add(self):
        print("Transaction added, refreshing transaction-related data...")
        self.refresh_data()

    def did_mount(self):
        super().did_mount()
        self.user_id = self.user_data.user_id
        self.refresh_data()

    def refresh_data(self):
        print("Refreshing transaction data...")
        self.returned_trans = self.trans_funcs.getTransactionList(self.user_id)
        self.transDetails = []
        self.prepare_transaction_details()

        new_data_rows = self.create_transaction_rows()

        if not new_data_rows:
            new_data_rows = [
                ft.DataRow(cells=[ft.DataCell(ft.Text("No transactions found", color="red"))] +
                           [ft.DataCell(ft.Text("")) for _ in range(5)])
            ]

        self.table.rows = new_data_rows
        self.page.update()
        print("Transaction table updated.")

    def prepare_transaction_details(self):
        for TID in self.returned_trans:
            details = self.trans_funcs.getTransactionDetails(TID)

            if details and len(details) == 1 and len(details[0]) == 5:
                budget_account_id = details[0][0]
                budget_account_name = self.trans_funcs.getBudgetAccountName(budget_account_id)
                full_details = list(details[0])
                full_details.insert(1, budget_account_name)
                self.transDetails.append(full_details)
            else:
                print(f"Skipping invalid details for TID: {TID}, Details: {details}")

    def create_transaction_rows(self):
        data_rows = []
        for row_data in self.transDetails:
            transaction_id = row_data[0]
            display_row = [
                row_data[0],
                row_data[1],
                f"${row_data[3]:.2f}",
                row_data[4],
                "Yes" if row_data[5] else "No",
            ]

            def delete_row(e, tid=transaction_id):
                print(f"Deleting transaction with ID: {tid}")
                self.trans_funcs.delete_transaction(tid)
                self.refresh_data()
                self.page.update()

            delete_button = ft.IconButton(icon=ft.Icons.DELETE, tooltip="Delete", on_click=delete_row)
            data_cells = [ft.DataCell(ft.Text(str(item))) for item in display_row]
            data_cells.append(ft.DataCell(delete_button))
            data_rows.append(ft.DataRow(cells=data_cells))
        return data_rows

    def refresh_after_vendor_add(self):
        print("Vendor added, refreshing vendor-related data...")
        self.add_transaction_dialog.open_and_refresh()
        self.refresh_data()

    def show_add_vendor_dialog(self, e):
        print("Opening AddVendor dialog")
        self.add_vendor_dialog.open = True
        self.page.update()

    def show_add_transaction_dialog(self, e):
        print("Opening AddTransaction dialog")
        self.page.dialog = self.add_transaction_dialog
        self.add_transaction_dialog.open_and_refresh()
