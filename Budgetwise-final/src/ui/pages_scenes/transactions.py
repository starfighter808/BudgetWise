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
        self.colors = colors
        self.vend_funcs = vend_funcs
        self.trans_funcs = trans_funcs
        self.amount_descending = False

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

        # Define each column as an individual variable.
        description_column = ft.DataColumn(
            label=ft.Text("Description", color=self.colors.BLUE_BACKGROUND)
        )

        amount_column = ft.DataColumn(
            label=ft.Row(
                controls=[
                    ft.Text("Amount", color=self.colors.BLUE_BACKGROUND),
                    ft.IconButton(
                        icon=ft.Icons.SORT,
                        icon_color=self.colors.BLUE_BACKGROUND,
                        on_click=lambda e: self.sort_transactions("transaction_amount")
                    )
                ],
                spacing=4,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        budget_account_column = ft.DataColumn(
            label=ft.Row(
                controls=[
                    ft.Text("Budget Account Name", color=self.colors.BLUE_BACKGROUND),
                    ft.IconButton(
                        icon=ft.Icons.SORT,
                        icon_color=self.colors.BLUE_BACKGROUND,
                        on_click=lambda e: self.sort_transactions("budget_account_id")
                    )
                ],
                spacing=4,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        transaction_date_column = ft.DataColumn(
            label=ft.Row(
                controls=[
                    ft.Text("Transaction Date", color=self.colors.BLUE_BACKGROUND),
                    ft.IconButton(
                        icon=ft.Icons.SORT,
                        icon_color=self.colors.BLUE_BACKGROUND,
                        on_click=lambda e: self.sort_transactions("transaction_date")
                    )
                ],
                spacing=4,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        recurring_column = ft.DataColumn(
            label=ft.Text("Recurring", color=self.colors.BLUE_BACKGROUND)
        )

        edit_column = ft.DataColumn(
            label=ft.Text("Edit", color=self.colors.BLUE_BACKGROUND)
        )

        delete_column = ft.DataColumn(
            label=ft.Text("Delete", color=self.colors.BLUE_BACKGROUND)
        )

        # Assemble the columns into a list.
        data_columns = [
            description_column,
            amount_column,
            budget_account_column,
            transaction_date_column,
            recurring_column,
            edit_column,
            delete_column,
        ]

        data_rows = self.create_transaction_rows()




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
            transaction_id = TID[0]
            
            # Expect details[0] to have 6 columns:
            # (budget_accounts_id, vendor_id, amount, description, recurring, transaction_date)
            if details and len(details) == 1 and len(details[0]) == 6:
                tuple_data = details[0]
                budget_account_id = tuple_data[0]
                vendor_id = tuple_data[1]  # Now we capture the vendor_id
                amount = tuple_data[2]
                description = tuple_data[3]
                recurring = tuple_data[4]
                transaction_date = tuple_data[5]
                budget_account_name = self.trans_funcs.getBudgetAccountName(budget_account_id)
                
                # Build final list with the desired order:
                # [ transaction_id, budget_account_name, budget_account_id, amount, description, transaction_date, recurring, vendor_id ]
                final_details = [
                    transaction_id,
                    budget_account_name,
                    budget_account_id,
                    amount,
                    description,
                    transaction_date,
                    recurring,
                    vendor_id
                ]
                
                print(final_details)
                self.transDetails.append(final_details)
            else:
                print(f"Skipping invalid details for TID: {TID}, Details: {details}")



    def create_transaction_rows(self):
        data_rows = []
        # Check if transDetails is empty
        if not self.transDetails:
            # Option 1: Return an empty list, so nothing gets rendered.
            # return data_rows
            
            # Option 2: Return a fallback row
            data_rows.append(
                ft.DataRow(
                    cells=(
                        [ft.DataCell(ft.Text("No transactions found", color="red"))] +
                        [ft.DataCell(ft.Text("")) for _ in range(6)]
                    )
                )
            )
            return data_rows
        for row_data in self.transDetails:
            # Assuming row_data is structured as:
            # [transaction_id, budget_account_name, budget_account_id, amount, description, transaction_date, recurring]
            transaction_id = row_data[0]
            display_row = [
                row_data[4],                           # Description (from index 4)
                f"${row_data[3]:.2f}",                 # Amount (from index 3)
                row_data[1],                           # Budget Account Name (from index 1)
                str(row_data[5])[:10],                 # Transaction Date (from index 5, trimmed)
                "Yes" if row_data[6] == 1 else "No",     # Recurring flag (from index 6)
            ]



            def delete_row(e, tid=transaction_id):
                print(f"Deleting transaction with ID: {tid}")
                self.trans_funcs.delete_transaction(tid)
                self.refresh_data()
                self.page.update()

            def edit_transaction(e, tid, transaction_row):
                # Instead of re-querying, use the provided transaction_row.
                self.add_transaction_dialog.load_transaction_info(transaction_row)
                self.add_transaction_dialog.open = True
                self.page.update()


            edit_button = ft.IconButton(
                icon=ft.Icons.EDIT,
                tooltip="Edit",
                icon_color=self.colors.GREEN_BUTTON,
                on_click=lambda e, row= row_data: edit_transaction(e, row[0], row)
            )

            delete_button = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Delete",
                icon_color=self.colors.ERROR_RED,
                on_click=delete_row
            )

            # Create DataCells for the display data.
            data_cells = [
                ft.DataCell(ft.Text(str(item), color=self.colors.TEXT_COLOR))
                for item in display_row
            ]
            # Append separate DataCells for the edit and delete buttons.
            data_cells.append(ft.DataCell(edit_button))
            data_cells.append(ft.DataCell(delete_button))
            
            # Now, data_cells will have 5 + 1 + 1 = 7 cells.
            data_rows.append(ft.DataRow(cells=data_cells))
        return data_rows


    def sort_transactions(self, sort_by):
        """
        Sorts the transactions stored in self.transDetails and then refreshes the table.
        
        Parameters:
            sort_by (str): The column to sort by. Accepts "budget_account_id", "transaction_amount", or "transaction_date".
        """
        if sort_by == "budget_account_id":
            # Budget Account ID is stored at index 2
            self.transDetails.sort(key=lambda x: x[2])
        elif sort_by == "transaction_amount":
            # Transaction amount is stored at index 3 (a numeric value)
            self.transDetails.sort(key=lambda x: x[3], reverse=self.amount_descending)
            # Toggle the sort order for next time.
            self.amount_descending = not self.amount_descending
        elif sort_by == "transaction_date":
            # Transaction date is stored at index 5
            self.transDetails.sort(key=lambda x: str(x[5])[:10], reverse=True)
        else:
            print("Unsupported sort key:", sort_by)
            return

        # Refresh the table rows after sorting.
        new_data_rows = self.create_transaction_rows()
        self.table.rows = new_data_rows
        self.page.update()




    def refresh_after_vendor_add(self):
        print("Vendor added, refreshing vendor-related data...")
        self.add_transaction_dialog.open_and_refresh()
        self.refresh_data()

    def show_add_vendor_dialog(self, e):
        print("Opening AddVendor dialog")
        self.add_vendor_dialog.fill_vendor_names()
        self.add_vendor_dialog.open = True
        self.page.update()

    def show_add_transaction_dialog(self, e):
        print("Opening AddTransaction dialog")
        self.page.dialog = self.add_transaction_dialog
        self.add_transaction_dialog.open_and_refresh()
    
    